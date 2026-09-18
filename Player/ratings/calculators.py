"""Rating calculators (player_gen.txt sections 7, 11, 12, 16).

Calculators are pure and deterministic: given the same DetailedPlayerAttributes,
they always return the same result and never mutate their input.
"""

import math

from Player.ratings.errors import MissingAttributeError, ValidationError
from Player.ratings.model import RatingResult, UnavailableRating
from Player.ratings.weights import (
    BATTING_WEIGHTS,
    FIELDING_WEIGHTS,
    MENTALITY_SUMMARY_WEIGHTS,
    PACE_BOWLING_WEIGHTS,
    ROLE_OVERALL_WEIGHTS,
    SPIN_BOWLING_WEIGHTS,
    WICKETKEEPING_WEIGHTS,
)


def round_half_up(value: float) -> int:
    """floor(value + 0.5), for nonnegative numbers (section 1)."""
    return math.floor(value + 0.5)


def clamp(value, lo, hi):
    return max(lo, min(hi, value))


def displayed_rating(raw: float) -> int:
    return clamp(round_half_up(raw), 0, 99)


def validate_attribute_value(path: str, value) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{path}: value must be numeric, got {type(value).__name__}")
    if not math.isfinite(value):
        raise ValidationError(f"{path}: value must be finite")
    if value < 0 or value > 99:
        raise ValidationError(f"{path}: value must be between 0 and 99 inclusive, got {value}")


def build_repertoire(pairs) -> dict:
    """Constructs a repertoire dict from an iterable of (deliveryId, rating)
    pairs, rejecting duplicate identifiers (section 7) instead of silently
    keeping the last one the way a plain dict literal would.
    """
    repertoire = {}
    for delivery_id, rating in pairs:
        if delivery_id in repertoire:
            raise ValidationError(f"Duplicate delivery identifier: {delivery_id!r}")
        repertoire[delivery_id] = rating
    return repertoire


def calculate_variation_quality(repertoire: dict) -> float:
    """section 7. `repertoire` holds only available deliveries; an
    unavailable delivery must simply be absent from the dict, not present
    with a fabricated value.
    """
    for delivery_id, rating in repertoire.items():
        validate_attribute_value(f"repertoire.{delivery_id}", rating)

    if not repertoire:
        return 0.0
    ratings = sorted(repertoire.values(), reverse=True)
    if len(ratings) == 1:
        return float(ratings[0])
    return 0.70 * ratings[0] + 0.30 * ratings[1]


def _resolve_pace_variation_quality(player) -> "float | None":
    repertoire = player.repertoire.get("pace")
    if repertoire is None:
        return None
    return calculate_variation_quality(repertoire)


def _resolve_spin_variation_quality(player) -> "float | None":
    repertoire = player.repertoire.get("spin")
    if repertoire is None:
        return None
    return calculate_variation_quality(repertoire)


_DERIVED_RESOLVERS = {
    "DERIVED.paceVariationQuality": _resolve_pace_variation_quality,
    "DERIVED.spinVariationQuality": _resolve_spin_variation_quality,
}


def _calculate_weighted_rating(player, weight_table, breakdown: bool = False) -> RatingResult:
    """The shared engine behind every calculateXRating function: rawRating =
    sum(attributeValue * weightPercent) / 100 (section 11), raising
    MissingAttributeError (listing every missing path, not just the first)
    if any required attribute is absent.
    """
    missing = []
    contributions = []
    raw_total = 0.0

    for path, weight in weight_table:
        if path in _DERIVED_RESOLVERS:
            value = _DERIVED_RESOLVERS[path](player)
        else:
            value = player.get(path)

        if value is None:
            missing.append(path)
            continue

        validate_attribute_value(path, value)
        contribution = value * weight / 100
        raw_total += contribution
        if breakdown:
            contributions.append((path, value, weight, contribution))

    if missing:
        raise MissingAttributeError(missing)

    return RatingResult(raw=raw_total, displayed=displayed_rating(raw_total), breakdown=contributions or None)


def calculate_batting_rating(player, breakdown: bool = False) -> RatingResult:
    return _calculate_weighted_rating(player, BATTING_WEIGHTS, breakdown)


def calculate_pace_bowling_rating(player, breakdown: bool = False) -> RatingResult:
    return _calculate_weighted_rating(player, PACE_BOWLING_WEIGHTS, breakdown)


def calculate_spin_bowling_rating(player, breakdown: bool = False) -> RatingResult:
    return _calculate_weighted_rating(player, SPIN_BOWLING_WEIGHTS, breakdown)


def calculate_fielding_rating(player, breakdown: bool = False) -> RatingResult:
    return _calculate_weighted_rating(player, FIELDING_WEIGHTS, breakdown)


def calculate_wicketkeeping_rating(player, breakdown: bool = False) -> RatingResult:
    return _calculate_weighted_rating(player, WICKETKEEPING_WEIGHTS, breakdown)


def calculate_mentality_rating(player, breakdown: bool = False) -> RatingResult:
    return _calculate_weighted_rating(player, MENTALITY_SUMMARY_WEIGHTS, breakdown)


def calculate_overall_rating(role: str, core_ratings: dict, breakdown: bool = False) -> RatingResult:
    """section 12. `core_ratings` holds RAW (unrounded) batting/bowling/
    fielding/wicketkeeping ratings - `bowling` must already be whichever of
    pace/spin is this player's primaryBowlingStyle; this function does not
    resolve that itself. Only core ratings with a nonzero weight for `role`
    are required - e.g. a specialist batter's overall never needs a
    wicketkeeping rating, present or not.
    """
    if role not in ROLE_OVERALL_WEIGHTS:
        raise ValidationError(f"Unknown role: {role!r}")

    weights = ROLE_OVERALL_WEIGHTS[role]
    missing = []
    contributions = []
    raw_total = 0.0

    for key, weight in weights.items():
        if weight == 0:
            continue
        value = core_ratings.get(key)
        if value is None:
            missing.append(key)
            continue
        validate_attribute_value(key, value)
        contribution = value * weight / 100
        raw_total += contribution
        if breakdown:
            contributions.append((key, value, weight, contribution))

    if missing:
        raise MissingAttributeError(missing)

    return RatingResult(raw=raw_total, displayed=displayed_rating(raw_total), breakdown=contributions or None)


def calculate_player_ratings(player, breakdown: bool = False) -> dict:
    """Convenience function: computes every discipline that has data present
    for this player, plus the role overall. Disciplines that raise
    MissingAttributeError (e.g. wicketkeeping for a non-keeper with no
    wicketkeeping.* attributes at all) come back as UnavailableRating instead
    of failing the whole call, matching section 15's "return a clear
    validation error or unavailable rating with missing paths."
    """
    results = {}

    def _try(key, func):
        try:
            results[key] = func()
        except MissingAttributeError as exc:
            results[key] = UnavailableRating(missing=exc.missing_paths)

    _try("batting", lambda: calculate_batting_rating(player, breakdown))
    if player.paceBowling:
        _try("paceBowling", lambda: calculate_pace_bowling_rating(player, breakdown))
    if player.spinBowling:
        _try("spinBowling", lambda: calculate_spin_bowling_rating(player, breakdown))
    _try("fielding", lambda: calculate_fielding_rating(player, breakdown))
    if player.wicketkeeping:
        _try("wicketkeeping", lambda: calculate_wicketkeeping_rating(player, breakdown))
    _try("mentality", lambda: calculate_mentality_rating(player, breakdown))

    bowling_raw = None
    bowling_key = {"pace": "paceBowling", "spin": "spinBowling"}.get(player.primary_bowling_style)
    if bowling_key and isinstance(results.get(bowling_key), RatingResult):
        bowling_raw = results[bowling_key].raw

    def _raw(key):
        result = results.get(key)
        return result.raw if isinstance(result, RatingResult) else None

    core_ratings = {
        "batting": _raw("batting"),
        "bowling": bowling_raw,
        "fielding": _raw("fielding"),
        "wicketkeeping": _raw("wicketkeeping"),
    }
    _try("overall", lambda: calculate_overall_rating(player.role, core_ratings, breakdown))

    return results
