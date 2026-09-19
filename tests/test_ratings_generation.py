"""Tests for Phase 2: reverse-engineering detailed attributes for an
already-generated Player, such that recomputing the relevant rating from
them reproduces exactly the same core bowling/fielding numbers. Batting is
the one exception - see test_batting_rating_never_exceeds_core_rating below.
"""

import random

from Player.player import DomesticPlayer, Player
from Player.ratings import (
    calculate_batting_rating,
    calculate_fielding_rating,
    calculate_pace_bowling_rating,
    calculate_spin_bowling_rating,
)
from Player.ratings.generation import infer_role, generate_detailed_attributes
from app.game.player_pool import create_pool


def _bowling_rating(player, detail):
    if player.bowling_type == "Pacer":
        return calculate_pace_bowling_rating(detail)
    return calculate_spin_bowling_rating(detail)


def test_generated_details_reproduce_bowling_and_fielding_core_ratings():
    random.seed(2026)
    mismatches = []
    for i in range(500):
        player = DomesticPlayer(i)
        detail = generate_detailed_attributes(player)

        bowling = _bowling_rating(player, detail)
        fielding = calculate_fielding_rating(detail)

        if bowling.displayed != player.bowling:
            mismatches.append(("bowling", player.bowling, bowling.displayed))
        if fielding.displayed != player.fielding:
            mismatches.append(("fielding", player.fielding, fielding.displayed))

    assert mismatches == []


def test_batting_rating_never_exceeds_core_rating():
    """batting.vsPace/vsSpin (a 1-10 matchup rating - see generation.py) blend
    into calculate_batting_rating per BATTING_VS_BLEND (weights.py): base +
    vsSpin*(vsSpin/10) + vsPace*(vsPace/10) weight shares. That blend factor
    maxes out at exactly 1.0 only when vsPace == vsSpin == 10, so it can only
    ever shrink the base rating, never restore it above it - generation.py
    solves the base batting attributes against player.batting/blend so the
    result still lands exactly on player.batting whenever that's achievable
    within the 0-99 attribute ceiling, but not guaranteed for every player the
    smaller BATTING_VS_BLEND's vsSpin/vsPace shares are, the closer this gets
    to 100% (accepted trade-off, not a bug - see conversation history). This
    locks in the two invariants that must always hold regardless of whatever
    BATTING_VS_BLEND is currently set to: batting never displays above the
    Phase 1 core value, and the undershoot rate doesn't silently worsen.
    """
    random.seed(2026)
    mismatches = 0
    for i in range(2000):
        player = DomesticPlayer(i)
        detail = generate_detailed_attributes(player)
        batting = calculate_batting_rating(detail)

        assert batting.displayed <= player.batting
        if batting.displayed != player.batting:
            mismatches += 1

    assert mismatches <= 25  # ~7/2000 at this seed today; regression guard, not a target


def test_every_player_gets_exactly_one_bowling_style_detail():
    random.seed(3)
    for i in range(50):
        player = DomesticPlayer(i)
        detail = generate_detailed_attributes(player)
        if player.bowling_type == "Pacer":
            assert detail.paceBowling
            assert not detail.spinBowling
            assert "pace" in detail.repertoire
            assert "spin" not in detail.repertoire
        else:
            assert detail.spinBowling
            assert not detail.paceBowling
            assert "spin" in detail.repertoire
            assert "pace" not in detail.repertoire


def test_only_wicketkeepers_get_wicketkeeping_detail():
    random.seed(4)
    saw_keeper = False
    for i in range(200):
        player = DomesticPlayer(i)
        detail = generate_detailed_attributes(player)
        if player.position == "Wicketkeeper":
            saw_keeper = True
            assert detail.wicketkeeping
        else:
            assert detail.wicketkeeping == {}
    assert saw_keeper, "expected at least one wicketkeeper in 200 random players"


def test_role_inference_matches_position_and_skill_split():
    def make(batting, bowling, position, bowling_type="Pacer"):
        return Player(
            player_id=1,
            json_data={
                "name": "X", "batting": batting, "bowling": bowling, "fielding": 60,
                "position": position, "fame": 50, "estimated_price": 10,
                "batting_hand": "Right", "bowling_type": bowling_type, "bowling_style": "Medium",
                "batting_order": "Top Order", "selling_price": 0,
            },
        )

    assert infer_role(make(80, 40, "Batsmen")) == ("specialistBatter", "none")
    assert infer_role(make(40, 80, "Bowler", "Spinner")) == ("specialistBowler", "spin")
    assert infer_role(make(85, 30, "Wicketkeeper")) == ("wicketkeeperBatter", "none")
    assert infer_role(make(80, 60, "Allrounder"))[0] == "battingAllRounder"
    assert infer_role(make(55, 80, "Allrounder"))[0] == "bowlingAllRounder"
    assert infer_role(make(68, 65, "Allrounder"))[0] == "balancedAllRounder"
    assert infer_role(make(45, 30, "Trainee")) == ("specialistBatter", "none")
    assert infer_role(make(30, 45, "Trainee", "Spinner"))[0] == "specialistBowler"


def test_same_seed_gives_the_same_detailed_attributes():
    pool_a = create_pool(seed=808, count=15)
    pool_b = create_pool(seed=808, count=15)

    for player_id, detail_a in pool_a.detailed.items():
        detail_b = pool_b.detailed[player_id]
        assert detail_a.role == detail_b.role
        assert detail_a.batting == detail_b.batting
        assert detail_a.paceBowling == detail_b.paceBowling
        assert detail_a.spinBowling == detail_b.spinBowling
        assert detail_a.fielding == detail_b.fielding
        assert detail_a.physical == detail_b.physical
        assert detail_a.mentality == detail_b.mentality
        assert detail_a.repertoire == detail_b.repertoire


def test_pool_detail_covers_every_generated_player():
    pool = create_pool(seed=55, count=40)
    assert set(pool.detailed.keys()) == {p.player_id for p in pool.generation.list_of_players}
