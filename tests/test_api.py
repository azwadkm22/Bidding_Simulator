import pytest
from fastapi.testclient import TestClient

from app.api import game as game_api
from app.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def disable_live_clock(monkeypatch):
    # These tests drive the game synchronously through direct API calls; the
    # autonomous live clock (services/live_clock.py) is covered separately in
    # test_live_clock.py and would otherwise leave background tasks running
    # past the end of each test here.
    monkeypatch.setattr(game_api.live_clock, "start", lambda session: None)


def test_new_game_returns_playable_state():
    response = client.post("/api/game/new")
    assert response.status_code == 200
    state = response.json()

    assert state["phase"] == "on_block"
    assert state["current_player"] is not None
    assert state["current_price"] == 10
    assert state["available_actions"] == ["bid", "pass", "skip"]
    assert len(state["rivals"]) == 12
    assert isinstance(state["seed"], int)


def test_new_game_with_explicit_seed_reproduces_the_same_pool():
    state_a = client.post("/api/game/new", json={"seed": 999}).json()
    state_b = client.post("/api/game/new", json={"seed": 999}).json()

    assert state_a["seed"] == state_b["seed"] == 999
    assert state_a["current_player"]["name"] == state_b["current_player"]["name"]
    assert [r["name"] for r in state_a["rivals"]] == [r["name"] for r in state_b["rivals"]]


def test_get_game_returns_same_state():
    session_id = client.post("/api/game/new").json()["session_id"]
    response = client.get(f"/api/game/{session_id}")
    assert response.status_code == 200
    assert response.json()["session_id"] == session_id


def test_unknown_session_returns_404():
    response = client.get("/api/game/does-not-exist")
    assert response.status_code == 404


def test_invalid_bid_returns_400_with_message():
    session_id = client.post("/api/game/new").json()["session_id"]
    response = client.post(f"/api/game/{session_id}/bid", json={"increment": -5})
    assert response.status_code == 400
    assert "positive" in response.json()["detail"]


def test_team_detail_returns_full_squad_for_valid_key():
    state = client.post("/api/game/new").json()
    session_id = state["session_id"]
    rival_key = state["rivals"][0]["key"]

    response = client.get(f"/api/game/{session_id}/teams/{rival_key}")
    assert response.status_code == 200
    detail = response.json()
    assert detail["key"] == rival_key
    assert "squad" in detail
    assert "composition" in detail

    user_response = client.get(f"/api/game/{session_id}/teams/user")
    assert user_response.status_code == 200
    assert user_response.json()["key"] == "user"


def test_team_detail_unknown_key_returns_404():
    session_id = client.post("/api/game/new").json()["session_id"]
    response = client.get(f"/api/game/{session_id}/teams/does-not-exist")
    assert response.status_code == 404


def test_starting_eleven_unavailable_for_empty_squad():
    session_id = client.post("/api/game/new").json()["session_id"]
    response = client.get(f"/api/game/{session_id}/teams/user/starting-eleven")
    assert response.status_code == 200
    data = response.json()
    assert data["key"] == "user"
    assert data["available"] is False
    assert data["reason"]
    assert data["lineup"] == []


def test_starting_eleven_unknown_team_returns_404():
    session_id = client.post("/api/game/new").json()["session_id"]
    response = client.get(f"/api/game/{session_id}/teams/does-not-exist/starting-eleven")
    assert response.status_code == 404


def test_starting_eleven_available_after_full_squad():
    state = client.post("/api/game/new").json()
    session_id = state["session_id"]
    state = client.post(f"/api/game/{session_id}/complete-simulation").json()

    big_team = next((r for r in state["rivals"] if r["squad_size"] >= 11), None)
    assert big_team is not None, "expected at least one 11+ player squad after a full simulation"

    response = client.get(f"/api/game/{session_id}/teams/{big_team['key']}/starting-eleven")
    assert response.status_code == 200
    data = response.json()
    if data["available"]:
        assert len(data["lineup"]) == 11
        assert data["batting_rating"] is not None
        assert data["bowling_rating"] is not None
        assert data["fielding_rating"] is not None
    else:
        assert data["reason"]


def test_remaining_players_matches_players_remaining_count():
    state = client.post("/api/game/new").json()
    session_id = state["session_id"]

    response = client.get(f"/api/game/{session_id}/players/remaining")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == state["players_remaining"]
    assert len(data["players"]) == data["count"]
    # Sorted by estimated value, most valuable first.
    prices = [p["estimated_price"] for p in data["players"]]
    assert prices == sorted(prices, reverse=True)


def test_complete_simulation_finishes_the_whole_game():
    session_id = client.post("/api/game/new").json()["session_id"]

    response = client.post(f"/api/game/{session_id}/complete-simulation")
    assert response.status_code == 200
    state = response.json()
    assert state["phase"] == "game_over"
    assert state["current_player"] is None
    assert state["available_actions"] == []


def test_summary_after_complete_simulation():
    session_id = client.post("/api/game/new").json()["session_id"]
    state = client.post(f"/api/game/{session_id}/complete-simulation").json()

    response = client.get(f"/api/game/{session_id}/summary")
    assert response.status_code == 200
    summary = response.json()

    total_sold = sum(t["squad_size"] for t in summary["teams"])
    assert len(summary["sold_players"]) == total_sold
    assert total_sold + summary["unsold_count"] == 250

    # sold_players sorted by price paid, most expensive first
    prices = [p["selling_price"] for p in summary["sold_players"]]
    assert prices == sorted(prices, reverse=True)

    assert len(summary["teams"]) == 13  # user + 12 rivals
    user_team = next(t for t in summary["teams"] if t["key"] == "user")
    assert user_team["is_user"] is True
    assert "starting_eleven" in user_team

    # every sold player entry identifies its buyer
    for entry in summary["sold_players"]:
        assert entry["buyer_key"] in [t["key"] for t in summary["teams"]]


def test_pause_and_resume_toggle_paused_flag():
    session_id = client.post("/api/game/new").json()["session_id"]

    response = client.post(f"/api/game/{session_id}/pause")
    assert response.status_code == 200
    assert response.json()["paused"] is True

    response = client.post(f"/api/game/{session_id}/resume")
    assert response.status_code == 200
    assert response.json()["paused"] is False


def test_skip_resolves_the_player_instantly():
    session_id = client.post("/api/game/new").json()["session_id"]
    response = client.post(f"/api/game/{session_id}/skip")
    assert response.status_code == 200
    state = response.json()
    assert state["phase"] in ("sold", "unsold")
    assert state["available_actions"] == ["advance"]


def test_pass_then_bid_progress_the_auction():
    session_id = client.post("/api/game/new").json()["session_id"]
    response = client.post(f"/api/game/{session_id}/pass")
    assert response.status_code == 200

    response = client.post(f"/api/game/{session_id}/bid", json={"increment": 10})
    assert response.status_code == 200
    assert response.json()["current_price"] > 10
