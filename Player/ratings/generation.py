"""Phase 2: generate detailed attributes for an already-generated Player.

Phase 1 (existing, untouched) generates a Player's core batting/bowling/
fielding numbers. Phase 2 reverse-engineers a full detailed attribute
breakdown - the tables in player_gen.txt sections 4-9 - such that recomputing
the relevant calculateXRating() from the generated details reproduces exactly
those same three core numbers (as displayed/rounded ratings). Shared
physical/mentality attributes are generated once per player and reused
consistently across every discipline that references them, so this is a
genuine constraint-satisfaction step, not independent per-discipline
randomness.

Uses the bare `random` module (like the rest of Player/Team generation), so
"same seed" for a pool means Phase 2 continues the same seeded stream Phase 1
just used, rather than being reseeded independently.
"""

import random

from Player.player import Player
from Player.ratings.calculators import calculate_variation_quality, clamp
from Player.ratings.model import DetailedPlayerAttributes
from Player.ratings.weights import (
    BATTING_VS_BLEND,
    BATTING_WEIGHTS,
    FIELDING_WEIGHTS,
    KEEPING_LEVEL_BLEND,
    PACE_BOWLING_WEIGHTS,
    SPIN_BOWLING_WEIGHTS,
    WICKETKEEPING_WEIGHTS,
)

ALLROUNDER_MARGIN = 8

PACE_DELIVERY_TYPES = ["slowerBall", "offCutter", "legCutter", "reverseSwing"]
SPIN_DELIVERY_TYPES = ["googly", "doosra", "slider", "flipper", "armBall", "topSpinner"]

# Shared attribute paths referenced by the core weight tables - generated
# once per player, before any discipline is solved, so every formula that
# references e.g. mentality.composure sees the exact same value. Each is
# anchored to whichever discipline's target weighs it most heavily (not a
# single blended "overall" of all three core stats): a player with, say,
# great fielding but mediocre batting/bowling would otherwise get a
# reflexes/anticipation value anchored way below what fielding needs,
# forcing fielding's slack attribute to overcorrect past 99.
SHARED_ATTRIBUTE_ANCHORS = {
    "physical.stamina": "bowling",
    "physical.reflexes": "fielding",
    "physical.runningSpeed": "fielding",
    "physical.agility": "fielding",
    "physical.strength": "batting",
    "physical.footwork": "batting",
    "physical.balance": "batting",
    "mentality.composure": "batting",
    "mentality.concentration": "batting",
    "mentality.decisionMaking": "batting",
    "mentality.discipline": "batting",
    "mentality.tacticalAwareness": "bowling",
    "mentality.anticipation": "fielding",
}

# Shared attributes that exist per player_gen.txt section 3 but aren't
# referenced by any weight table here - generated for a complete profile,
# with no target to satisfy. (physical.acceleration was removed entirely -
# no longer generated at all, not even unconstrained.)
UNCONSTRAINED_PHYSICAL_ATTRS = ["recovery"]
UNCONSTRAINED_MENTALITY_ATTRS = [
    "adaptability", "resilience", "gameReading", "leadership",
    "aggressiveness",  # moved here from traits - see generate_detailed_attributes
]

def infer_role(player: Player) -> tuple:
    """Maps the existing position/bowling_type onto player_gen.txt's role and
    primaryBowlingStyle taxonomy - see the design discussion: Allrounder
    splits by which of batting/bowling is clearly ahead (ALLROUNDER_MARGIN),
    and Trainee (not in the new role list) maps to whichever specialism its
    higher stat suggests. `bowling_style` is always resolved from
    bowling_type since every player has one regardless of role; a role's
    primaryBowlingStyle can still legitimately be "none" (its overall simply
    doesn't weight bowling) even though bowling detail is still generated for
    every player (see generate_detailed_attributes).
    """
    bowling_style = "pace" if player.bowling_type == "Pacer" else "spin"

    if player.position == "Batsmen":
        return "specialistBatter", "none"
    if player.position == "Bowler":
        return "specialistBowler", bowling_style
    if player.position == "Wicketkeeper":
        return "wicketkeeperBatter", "none"
    if player.position == "Allrounder":
        if player.batting - player.bowling > ALLROUNDER_MARGIN:
            role = "battingAllRounder"
        elif player.bowling - player.batting > ALLROUNDER_MARGIN:
            role = "bowlingAllRounder"
        else:
            role = "balancedAllRounder"
        return role, bowling_style
    # Trainee
    if player.batting >= player.bowling:
        return "specialistBatter", "none"
    return "specialistBowler", bowling_style


def _natural_value(center: float, spread: float) -> float:
    if spread <= 0:
        return clamp(round(center), 0, 99)
    return clamp(round(random.gauss(center, spread)), 0, 99)


def _spread_for_target(target: float, base_spread: float = 8.0) -> float:
    # Shrinks near the 0/99 boundaries so clamping can't systematically bias
    # the average of the naturally-generated attributes away from the target,
    # which would force the slack attribute out of [0, 99] to compensate.
    return max(0.0, min(base_spread, target, 99 - target))


def _generate_natural_repertoire(delivery_types: list, target: float, spread: float) -> dict:
    count = random.choice([1, 2, 2, 3])
    count = min(count, len(delivery_types))
    chosen = random.sample(delivery_types, count)
    return {delivery: _natural_value(target, spread) for delivery in chosen}


def _solve_discipline(weight_table: list, target: float, fixed: dict, repertoire_types=None, max_passes: int = 8):
    """Returns (attributes: dict[bare attribute name -> value], repertoire: dict | None).

    `fixed` maps full paths ("physical.stamina", ...) already decided for
    this player and treated as constants here. Every other attribute in
    `weight_table` (including the DERIVED variation-quality slot, via its
    generated repertoire) is generated naturally around `target`, then
    nudged - proportionally to weight, together, in the same pass - until the
    weighted total lands exactly on `target`.

    Spreading the correction across every free attribute (rather than
    concentrating it in one "slack" attribute) matters because some of the
    weight in `weight_table` is spoken for by attributes fixed for a
    *different* discipline's benefit (e.g. mentality.composure is anchored to
    batting but still counted at 2% in bowling) - a single slack attribute
    can occasionally need to move past 0 or 99 to close that gap alone, while
    dividing the same correction across ten-plus attributes essentially never
    does.
    """
    free_attrs = []  # (attribute_name, weight)
    derived_weight = None
    raw_fixed = 0.0

    for path, weight in weight_table:
        category, _, attribute = path.partition(".")
        if path in fixed:
            raw_fixed += fixed[path] * weight / 100
        elif category == "DERIVED":
            derived_weight = weight
        else:
            free_attrs.append((attribute, weight))

    spread = _spread_for_target(target, base_spread=5.0)
    values = {name: _natural_value(target, spread) for name, _ in free_attrs}
    repertoire = _generate_natural_repertoire(repertoire_types, target, spread) if derived_weight is not None else None

    total_free_weight = sum(weight for _, weight in free_attrs) + (derived_weight or 0)

    for _ in range(max_passes):
        raw = raw_fixed + sum(values[name] * weight / 100 for name, weight in free_attrs)
        if derived_weight is not None:
            raw += calculate_variation_quality(repertoire) * derived_weight / 100

        error = target - raw
        if abs(error) < 1e-9 or total_free_weight <= 0:
            break

        delta = error * 100 / total_free_weight
        for name, _ in free_attrs:
            values[name] = clamp(values[name] + delta, 0, 99)
        if repertoire:
            repertoire = {delivery: clamp(rating + delta, 0, 99) for delivery, rating in repertoire.items()}

    return values, repertoire


def generate_detailed_attributes(player: Player) -> DetailedPlayerAttributes:
    role, primary_bowling_style = infer_role(player)
    overall_level = (player.batting + player.bowling + player.fielding) / 3
    discipline_target = {"batting": player.batting, "bowling": player.bowling, "fielding": player.fielding}

    physical = {}
    mentality = {}
    for path, discipline in SHARED_ATTRIBUTE_ANCHORS.items():
        category, _, attribute = path.partition(".")
        anchor = discipline_target[discipline]
        value = _natural_value(anchor, _spread_for_target(anchor, base_spread=10.0))
        (physical if category == "physical" else mentality)[attribute] = value

    physical.update({attr: _natural_value(overall_level, 15) for attr in UNCONSTRAINED_PHYSICAL_ATTRS})
    mentality.update({attr: _natural_value(overall_level, 15) for attr in UNCONSTRAINED_MENTALITY_ATTRS})

    fixed = {f"physical.{k}": v for k, v in physical.items() if f"physical.{k}" in SHARED_ATTRIBUTE_ANCHORS}
    fixed.update({f"mentality.{k}": v for k, v in mentality.items() if f"mentality.{k}" in SHARED_ATTRIBUTE_ANCHORS})

    detail = DetailedPlayerAttributes(
        player_id=player.player_id,
        role=role,
        primary_bowling_style=primary_bowling_style,
        physical=physical,
        mentality=mentality,
    )

    # vsPace/vsSpin are a 1-10 matchup rating, generated before the batting
    # weight table is solved, then calculate_batting_rating (calculators.py)
    # blends them on top of the weighted rating below per BATTING_VS_BLEND
    # (weights.py - imported here too, so this can never drift out of sync
    # with calculators.py). To still land on player.batting exactly, solve
    # BATTING_WEIGHTS for whatever pre-blend value survives that blend to
    # produce the real target, rather than solving for the target itself.
    vs_center = 1 + (player.batting / 99) * 9
    vs_spread = max(0.0, min(2.5, vs_center - 1, 10 - vs_center))
    vs_pace = int(clamp(round(random.gauss(vs_center, vs_spread)), 1, 10)) if vs_spread > 0 else int(round(vs_center))
    vs_spin = int(clamp(round(random.gauss(vs_center, vs_spread)), 1, 10)) if vs_spread > 0 else int(round(vs_center))
    blend = (
        BATTING_VS_BLEND["base"]
        + BATTING_VS_BLEND["vsSpin"] * (vs_spin / 10)
        + BATTING_VS_BLEND["vsPace"] * (vs_pace / 10)
    )
    pre_blend_target = player.batting / blend if blend > 0 else player.batting

    detail.batting, _ = _solve_discipline(BATTING_WEIGHTS, pre_blend_target, fixed)
    detail.batting["vsPace"] = vs_pace
    detail.batting["vsSpin"] = vs_spin

    if player.bowling_type == "Pacer":
        detail.paceBowling, pace_repertoire = _solve_discipline(
            PACE_BOWLING_WEIGHTS, player.bowling, fixed, PACE_DELIVERY_TYPES
        )
        detail.repertoire["pace"] = pace_repertoire
    else:
        detail.spinBowling, spin_repertoire = _solve_discipline(
            SPIN_BOWLING_WEIGHTS, player.bowling, fixed, SPIN_DELIVERY_TYPES
        )
        detail.repertoire["spin"] = spin_repertoire

    detail.fielding, _ = _solve_discipline(FIELDING_WEIGHTS, player.fielding, fixed)

    if player.position == "Wicketkeeper":
        # No existing core scalar to preserve here - just a natural profile
        # around the player's batting/fielding level, weighted per
        # KEEPING_LEVEL_BLEND (weights.py) - see app/game/view.py for the
        # other side that must stay in sync with this same formula.
        keeping_level = (
            KEEPING_LEVEL_BLEND["batting"] * player.batting + KEEPING_LEVEL_BLEND["fielding"] * player.fielding
        )
        detail.wicketkeeping = {}
        for path, _weight in WICKETKEEPING_WEIGHTS:
            category, _, attribute = path.partition(".")
            if category != "wicketkeeping":
                continue
            detail.wicketkeeping[attribute] = _natural_value(keeping_level, 10)

    # Every state value starts flat at 50 rather than randomized - these are
    # meant to change during play (not implemented yet), not vary at
    # generation time.
    detail.state = {"confidence": 50, "form": 50, "morale": 50, "fitness": 50}

    return detail
