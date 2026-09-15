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
