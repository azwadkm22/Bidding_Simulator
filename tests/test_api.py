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


def test_generate_pool_returns_summary():
    response = client.post("/api/players/generate", json={"seed": 321, "count": 30})
    assert response.status_code == 200
    summary = response.json()

    assert summary["seed"] == 321
    assert summary["count"] == 30
    assert sum(summary["position_counts"].values()) == 30
    assert len(summary["top_batsmen"]) <= 10
    assert "pool_id" in summary


def test_generate_pool_same_seed_gives_same_summary():
    summary_a = client.post("/api/players/generate", json={"seed": 111, "count": 25}).json()
    summary_b = client.post("/api/players/generate", json={"seed": 111, "count": 25}).json()

    assert summary_a["top_batsmen"] == summary_b["top_batsmen"]
    assert summary_a["position_counts"] == summary_b["position_counts"]


def test_get_pool_players_matches_summary_count():
    summary = client.post("/api/players/generate", json={"seed": 5, "count": 15}).json()
    pool_id = summary["pool_id"]

    response = client.get(f"/api/players/{pool_id}/players")
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 15
    assert len(data["players"]) == 15


def test_unknown_pool_returns_404():
    response = client.get("/api/players/does-not-exist/summary")
    assert response.status_code == 404


def test_player_detail_returns_ratings_and_attributes():
    summary = client.post("/api/players/generate", json={"seed": 606, "count": 20}).json()
    pool_id = summary["pool_id"]
    player_id = summary["most_expensive"][0]["player_id"]

    response = client.get(f"/api/players/{pool_id}/players/{player_id}/detail")
    assert response.status_code == 200
    detail = response.json()

    assert detail["player_id"] == player_id
    assert detail["core"]["batting"] >= 0
    # batting can undershoot (never exceed) the core stat - see
    # test_batting_rating_never_exceeds_core_rating in test_ratings_generation.py.
    assert detail["ratings"]["batting"]["displayed"] <= detail["core"]["batting"]
    assert detail["role"] in (
        "specialistBatter", "specialistBowler", "battingAllRounder",
        "bowlingAllRounder", "balancedAllRounder", "wicketkeeperBatter",
    )
    # exactly one bowling-style attribute set is populated
    has_pace = bool(detail["attributes"]["paceBowling"])
    has_spin = bool(detail["attributes"]["spinBowling"])
    assert has_pace != has_spin
    bowling_key = "paceBowling" if has_pace else "spinBowling"
    assert detail["ratings"][bowling_key]["displayed"] == detail["core"]["bowling"]
    assert detail["ratings"]["fielding"]["displayed"] == detail["core"]["fielding"]


def test_player_detail_unknown_player_returns_404():
    summary = client.post("/api/players/generate", json={"seed": 7, "count": 10}).json()
    pool_id = summary["pool_id"]
    response = client.get(f"/api/players/{pool_id}/players/999999/detail")
    assert response.status_code == 404


def test_player_detail_unknown_pool_returns_404():
    response = client.get("/api/players/does-not-exist/players/0/detail")
    assert response.status_code == 404


def test_weight_tables_returns_every_table_and_batting_vs_blend():
    response = client.get("/api/players/weight-tables")
    assert response.status_code == 200
    data = response.json()

    assert set(data["tables"].keys()) == {
        "batting", "paceBowling", "spinBowling", "fielding",
        "wicketkeeping", "mentalitySummary", "physicalSummary",
    }
    assert sum(weight for _, weight in data["tables"]["batting"]) == 100
    assert set(data["batting_vs_blend"].keys()) == {"base", "vsSpin", "vsPace"}
    assert data["role_overall"]["specialistBatter"]["batting"] == 85


def test_preview_computes_ratings_with_breakdown_and_no_side_effects():
    body = {
        "role": "specialistBatter",
        "primary_bowling_style": "none",
        "attributes": {
            "batting": {
                "timing": 80, "shotSelection": 75, "defensiveTechnique": 70,
                "attackingTechnique": 72, "placement": 68, "offside": 65,
                "legside": 66, "straight": 67, "vsSpin": 7, "vsPace": 8,
            },
            "physical": {
                "strength": 60, "footwork": 65, "runningSpeed": 70,
                "agility": 68, "stamina": 62, "balance": 63,
            },
            "mentality": {"composure": 75, "concentration": 70, "decisionMaking": 66, "discipline": 64},
        },
    }
    response = client.post("/api/players/preview", json=body)
    assert response.status_code == 200
    data = response.json()

    batting = data["ratings"]["batting"]
    assert batting["unavailable"] is False
    assert batting["breakdown"] is not None
    breakdown_paths = {entry["path"] for entry in batting["breakdown"]}
    assert "batting.timing" in breakdown_paths
    assert "physical.strength" in breakdown_paths

    # fielding attributes were never supplied, so it comes back unavailable
    # rather than erroring the whole request.
    assert data["ratings"]["fielding"]["unavailable"] is True
    assert "fielding.catching" in data["ratings"]["fielding"]["missing"]


def test_create_custom_player_adds_to_pool_and_uses_computed_core_stats():
    summary = client.post("/api/players/generate", json={"seed": 1, "count": 10}).json()
    pool_id = summary["pool_id"]

    body = {
        "role": "specialistBatter",
        "primary_bowling_style": "none",
        "name": "Test Custom Batter",
        "position": "Batsmen",
        "batting_hand": "Right",
        "bowling_type": "Pacer",
        "batting_order": "Opener",
        "fame": 50,
        "attributes": {
            "batting": {
                "timing": 90, "shotSelection": 88, "defensiveTechnique": 85,
                "attackingTechnique": 87, "placement": 84, "offside": 82,
                "legside": 83, "straight": 86, "vsSpin": 9, "vsPace": 9,
            },
            "physical": {"strength": 80, "footwork": 82, "runningSpeed": 78, "agility": 79, "stamina": 77, "balance": 81},
            "mentality": {"composure": 85, "concentration": 84, "decisionMaking": 83, "discipline": 82},
        },
    }
    response = client.post(f"/api/players/{pool_id}/custom", json=body)
    assert response.status_code == 200
    created = response.json()

    assert created["name"] == "Test Custom Batter"
    assert created["core"]["batting"] > 0
    assert created["ratings"]["batting"]["displayed"] == created["core"]["batting"]

    players = client.get(f"/api/players/{pool_id}/players").json()
    assert players["count"] == 11
    assert any(p["player_id"] == created["player_id"] for p in players["players"])

    detail = client.get(f"/api/players/{pool_id}/players/{created['player_id']}/detail").json()
    assert detail["name"] == "Test Custom Batter"


def test_create_custom_player_unknown_pool_returns_404():
    body = {
        "role": "specialistBatter",
        "position": "Batsmen",
        "attributes": {"batting": {"timing": 50}},
    }
    response = client.post("/api/players/does-not-exist/custom", json=body)
    assert response.status_code == 404


def test_start_game_from_a_pregenerated_pool():
    summary = client.post("/api/players/generate", json={"seed": 42, "count": 20}).json()
    pool_id = summary["pool_id"]

    state = client.post("/api/game/new", json={"pool_id": pool_id}).json()
    assert state["seed"] == 42
    assert state["pool_id"] == pool_id

    # The auction draws players highest-price-first from the same pool, so
    # the current player on the block must be the pool's single most
    # expensive player.
    assert state["current_player"]["name"] == summary["most_expensive"][0]["name"]

    # The frontend uses this to fetch mid-auction player detail via the same
    # pool-scoped endpoint the generation screen uses.
    player_id = state["current_player"]["player_id"]
    detail = client.get(f"/api/players/{state['pool_id']}/players/{player_id}/detail")
    assert detail.status_code == 200
    assert detail.json()["player_id"] == player_id


def test_ad_hoc_seed_only_game_has_no_pool_id():
    state = client.post("/api/game/new", json={"seed": 123}).json()
    assert state["pool_id"] is None


def test_start_game_with_unknown_pool_id_returns_404():
    response = client.post("/api/game/new", json={"pool_id": "does-not-exist"})
    assert response.status_code == 404


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
