"""Tests for Player/ratings/ against player_gen.txt section 17's acceptance
criteria, plus the calculators' own contract (pure, deterministic, no
mutation).
"""

import copy

import pytest

from Player.ratings import (
    ValidationError,
    MissingAttributeError,
    build_repertoire,
    calculate_batting_rating,
    calculate_fielding_rating,
    calculate_mentality_rating,
    calculate_overall_rating,
    calculate_pace_bowling_rating,
    calculate_player_ratings,
    calculate_spin_bowling_rating,
    calculate_variation_quality,
    calculate_wicketkeeping_rating,
    DetailedPlayerAttributes,
    RatingResult,
    UnavailableRating,
)
from Player.ratings.calculators import _calculate_weighted_rating
from Player.ratings.weights import CORE_WEIGHT_TABLES, ROLE_OVERALL_WEIGHTS


def _full_batter(batting_value, composure=None, concentration=None):
    """A player with every batting-formula attribute set to the same value,
    with an empty pace repertoire (batting doesn't need one, but building a
    full player is convenient for calculate_player_ratings tests)."""
    return DetailedPlayerAttributes(
        player_id=1,
        role="specialistBatter",
        primary_bowling_style="none",
        batting={
            "timing": batting_value,
            "shotSelection": batting_value,
            "defensiveTechnique": batting_value,
            "attackingTechnique": batting_value,
            "placement": batting_value,
            "offside": batting_value,
            "legside": batting_value,
            "straight": batting_value,
        },
        mentality={
            "composure": composure if composure is not None else batting_value,
            "concentration": concentration if concentration is not None else batting_value,
            "decisionMaking": batting_value,
            "discipline": batting_value,
        },
        physical={
            "strength": batting_value, "runningSpeed": batting_value, "agility": batting_value,
            "stamina": batting_value, "footwork": batting_value, "balance": batting_value,
        },
    )


def _full_pace_bowler(value, repertoire_rating=None):
    detail = DetailedPlayerAttributes(
        player_id=2,
        role="specialistBowler",
        primary_bowling_style="pace",
        paceBowling={
            "pace": value,
            "lineControl": value,
            "lengthControl": value,
            "releaseConsistency": value,
            "swing": value,
            "seam": value,
            "bounce": value,
            "yorker": value,
            "bouncer": value,
            "disguise": value,
        },
        mentality={"tacticalAwareness": value, "composure": value},
        physical={"stamina": value},
    )
    detail.repertoire["pace"] = {} if repertoire_rating is None else {"slower": repertoire_rating}
    return detail


def _full_fielder(value):
    return DetailedPlayerAttributes(
        player_id=3,
        role="specialistBatter",
        primary_bowling_style="none",
        fielding={
            "catching": value,
            "groundFielding": value,
            "positioning": value,
            "throwAccuracy": value,
            "throwPower": value,
            "pickupAndRelease": value,
            "diving": value,
            "boundaryAwareness": value,
        },
        mentality={"anticipation": value},
        physical={"reflexes": value, "runningSpeed": value, "agility": value, "balance": value},
    )


# --- 1. Every weight table totals 100 -----------------------------------


def test_every_core_and_mentality_weight_table_totals_100():
    for name, table in CORE_WEIGHT_TABLES.items():
        assert sum(w for _, w in table) == 100, name


def test_every_role_overall_weight_table_totals_100():
    for role, weights in ROLE_OVERALL_WEIGHTS.items():
        assert sum(weights.values()) == 100, role


# --- 2/3/4. Uniform attribute value k => rating k -----------------------


@pytest.mark.parametrize("k", [0, 25, 50, 75, 99])
def test_uniform_batting_attributes_give_matching_rating(k):
    result = calculate_batting_rating(_full_batter(k))
    assert result.raw == pytest.approx(k)
    assert result.displayed == k


@pytest.mark.parametrize("k", [0, 25, 50, 75, 99])
def test_uniform_pace_bowling_attributes_with_matching_variation_give_k(k):
    result = calculate_pace_bowling_rating(_full_pace_bowler(k, repertoire_rating=k))
    assert result.raw == pytest.approx(k)
    assert result.displayed == k


def test_all_zero_with_empty_repertoire_gives_zero_pace_rating():
    result = calculate_pace_bowling_rating(_full_pace_bowler(0, repertoire_rating=None))
    assert result.raw == 0
    assert result.displayed == 0


def test_all_99_with_a_99_variation_gives_99_pace_rating():
    result = calculate_pace_bowling_rating(_full_pace_bowler(99, repertoire_rating=99))
    assert result.raw == pytest.approx(99)
    assert result.displayed == 99


# --- 5. Generic weighted-sum math ---------------------------------------


def test_weighted_example_80_70_90_gives_79():
    player = DetailedPlayerAttributes(player_id=9, role="specialistBatter", primary_bowling_style="none")
    player.batting = {"a": 80, "b": 70, "c": 90}
    table = [("batting.a", 50), ("batting.b", 30), ("batting.c", 20)]
    result = _calculate_weighted_rating(player, table)
    assert result.raw == pytest.approx(79)
    assert result.displayed == 79


# --- 6/7/8. Variation quality --------------------------------------------


@pytest.mark.parametrize(
    "repertoire, expected",
    [
        ({}, 0),
        ({"a": 85}, 85),
        ({"a": 85, "b": 70}, 80.5),
        ({"a": 85, "b": 70, "c": 60}, 80.5),  # 3rd+ ignored
    ],
)
def test_variation_quality_examples(repertoire, expected):
    assert calculate_variation_quality(repertoire) == pytest.approx(expected)


def test_available_zero_rated_variation_is_a_valid_entry():
    assert calculate_variation_quality({"a": 0}) == 0
    # Distinct from "no repertoire at all", which the pace/spin calculators
    # treat as MissingAttributeError - checked separately below.


def test_missing_repertoire_is_missing_not_empty():
    bowler = _full_pace_bowler(50)
    del bowler.repertoire["pace"]  # entirely absent, not even {}
    with pytest.raises(MissingAttributeError) as exc:
        calculate_pace_bowling_rating(bowler)
    assert "DERIVED.paceVariationQuality" in exc.value.missing_paths


def test_duplicate_variation_identifiers_are_rejected():
    with pytest.raises(ValidationError):
        build_repertoire([("googly", 80), ("slider", 70), ("googly", 60)])


def test_build_repertoire_accepts_unique_identifiers():
    repertoire = build_repertoire([("googly", 85), ("slider", 70)])
    assert repertoire == {"googly": 85, "slider": 70}


# --- 9/10. Role overall -------------------------------------------------


def test_balanced_allrounder_example_yields_79_36_raw_79_displayed():
    result = calculate_overall_rating("balancedAllRounder", {"batting": 82, "bowling": 76, "fielding": 88})
    assert result.raw == pytest.approx(79.36)
    assert result.displayed == 79


def test_overall_uses_raw_core_ratings_not_pre_rounded():
    # batting=82.9 (displays 83) and bowling=75.9 (displays 76): rounding
    # each one *before* combining shifts their sum up by 0.2 relative to the
    # raw sum (82.9+75.9=158.8 vs 83+76=159) - if calculate_overall_rating
    # were accidentally fed pre-rounded core ratings, the result would drift
    # from the value computed straight off the raw ratings.
    raw_result = calculate_overall_rating(
        "balancedAllRounder", {"batting": 82.9, "bowling": 75.9, "fielding": 88.0}
    )
    rounded_result = calculate_overall_rating(
        "balancedAllRounder", {"batting": 83, "bowling": 76, "fielding": 88}
    )
    assert raw_result.raw != pytest.approx(rounded_result.raw)


# --- 11/12. Validation ----------------------------------------------------


@pytest.mark.parametrize("bad_value", [-1, 100, float("nan"), float("inf"), "80", True])
def test_invalid_attribute_values_are_rejected(bad_value):
    player = _full_batter(50)
    player.batting["timing"] = bad_value
    with pytest.raises(ValidationError):
        calculate_batting_rating(player)


def test_missing_required_attribute_raises_with_paths():
    player = _full_batter(50)
    del player.batting["timing"]
    with pytest.raises(MissingAttributeError) as exc:
        calculate_batting_rating(player)
    assert "batting.timing" in exc.value.missing_paths


def test_unknown_role_is_a_validation_error():
    with pytest.raises(ValidationError):
        calculate_overall_rating("madeUpRole", {"batting": 50})


# --- 13. Ratings stay within [0, 99] -------------------------------------


@pytest.mark.parametrize("k", [0, 50, 99])
def test_ratings_stay_within_bounds(k):
    assert 0 <= calculate_batting_rating(_full_batter(k)).displayed <= 99
    assert 0 <= calculate_fielding_rating(_full_fielder(k)).displayed <= 99


# --- 14. Monotonicity -----------------------------------------------------


def test_raising_a_positively_weighted_input_cannot_lower_raw_rating():
    base = calculate_batting_rating(_full_batter(50))
    raised = _full_batter(50)
    raised.batting["timing"] = 90
    raised_result = calculate_batting_rating(raised)
    assert raised_result.raw >= base.raw


# --- 15. Traits/state/leadership/recovery excluded from base overall ----


def test_traits_and_temporary_state_do_not_affect_ratings():
    player_a = _full_batter(60)
    player_a.traits = {"aggressiveness": 10}
    player_a.state = {"confidence": 20, "form": 30, "fatigue": 90, "fitness": 10}
    player_a.physical["recovery"] = 5
    player_a.mentality["leadership"] = 5

    player_b = copy.deepcopy(player_a)
    player_b.traits = {"aggressiveness": 90}
    player_b.state = {"confidence": 90, "form": 90, "fatigue": 5, "fitness": 90}
    player_b.physical["recovery"] = 95
    player_b.mentality["leadership"] = 95

    assert calculate_batting_rating(player_a).raw == calculate_batting_rating(player_b).raw


# --- 16. Secondary bowling skills don't affect primary-style overall ----


def test_secondary_bowling_style_does_not_affect_role_overall():
    pace_player = _full_pace_bowler(70, repertoire_rating=70)
    pace_player.batting = _full_batter(70).batting  # specialistBowler overall needs batting too (10%)
    pace_player.fielding = _full_fielder(70).fielding
    pace_player.mentality.update(_full_batter(70).mentality)
    pace_player.mentality.update(_full_fielder(70).mentality)
    pace_player.physical.update(_full_fielder(70).physical)
    pace_player.physical.update(_full_batter(70).physical)
    ratings_before = calculate_player_ratings(pace_player)

    # A pace bowler shouldn't have spin data, but even if some were present
    # (e.g. leftover/irrelevant), it must not be used for their overall.
    pace_player.spinBowling = {"turn": 5, "lineControl": 5}  # deliberately poor
    ratings_after = calculate_player_ratings(pace_player)

    assert ratings_before["overall"].raw == ratings_after["overall"].raw


# --- 17. Shared attributes propagate without duplicated storage ---------


def test_shared_attribute_change_propagates_to_every_formula_using_it():
    player = _full_pace_bowler(70, repertoire_rating=70)
    before_pace = calculate_pace_bowling_rating(player).raw

    player.mentality["composure"] = 10  # shared by pace bowling (2%) - only one storage location
    after_pace = calculate_pace_bowling_rating(player).raw

    assert after_pace < before_pace


# --- 18. Missing keeping/bowling doesn't block an overall that excludes it


def test_specialist_batter_overall_does_not_need_bowling_or_keeping():
    core_ratings = {"batting": 80, "fielding": 60}  # no "bowling"/"wicketkeeping" keys at all
    result = calculate_overall_rating("specialistBatter", core_ratings)
    assert result.raw == pytest.approx(80 * 0.90 + 60 * 0.10)


def test_calculate_player_ratings_marks_unavailable_disciplines():
    player = _full_batter(70)  # no fielding attributes at all
    results = calculate_player_ratings(player)
    assert isinstance(results["fielding"], UnavailableRating)
    assert "fielding.catching" in results["fielding"].missing
    # But the overall (specialistBatter: fielding weight 15) still needs it -
    # so overall should also be unavailable here, and say why.
    assert isinstance(results["overall"], UnavailableRating)


# --- 19. Calculations do not mutate player data --------------------------


def test_calculators_do_not_mutate_input():
    player = _full_batter(70)
    snapshot = copy.deepcopy(player)
    calculate_batting_rating(player, breakdown=True)
    assert player == snapshot


def test_calculate_player_ratings_does_not_mutate_input():
    player = _full_pace_bowler(70, repertoire_rating=70)
    player.fielding = _full_fielder(70).fielding
    player.mentality.update(_full_fielder(70).mentality)
    player.physical.update(_full_fielder(70).physical)
    snapshot = copy.deepcopy(player)
    calculate_player_ratings(player, breakdown=True)
    assert player == snapshot


# --- Mentality summary and breakdown -------------------------------------


def test_mentality_summary_uses_its_own_weight_table():
    player = DetailedPlayerAttributes(
        player_id=5,
        role="specialistBatter",
        primary_bowling_style="none",
        mentality={
            "concentration": 60,
            "composure": 60,
            "decisionMaking": 60,
            "tacticalAwareness": 60,
            "adaptability": 60,
            "discipline": 60,
            "resilience": 60,
            "gameReading": 60,
        },
    )
    result = calculate_mentality_rating(player)
    assert result.raw == pytest.approx(60)
    assert result.displayed == 60


def test_breakdown_lists_path_value_weight_and_contribution():
    result = calculate_batting_rating(_full_batter(50), breakdown=True)
    assert result.breakdown is not None
    for path, value, weight, contribution in result.breakdown:
        assert contribution == pytest.approx(value * weight / 100)


def test_wicketkeeping_rating_uses_its_own_weight_table():
    player = DetailedPlayerAttributes(
        player_id=6,
        role="wicketkeeperBatter",
        primary_bowling_style="none",
        wicketkeeping={
            "glovework": 70,
            "standingUp": 70,
            "standingBack": 70,
            "stumping": 70,
            "legSideCollection": 70,
            "byesPrevention": 70,
        },
        fielding={"diving": 70, "catching": 70},
        physical={"reflexes": 70, "footwork": 70, "balance": 70},
        mentality={"anticipation": 70, "concentration": 70, "decisionMaking": 70},
    )
    result = calculate_wicketkeeping_rating(player)
    assert result.raw == pytest.approx(70)
    assert result.displayed == 70
