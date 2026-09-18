"""Weight tables from player_gen.txt sections 4-10 and 12.

Every table is a list of (path, weight_percent) pairs. A path is either
"<category>.<attribute>" (a stored attribute - category is one of batting,
paceBowling, spinBowling, fielding, wicketkeeping, physical, mentality) or
"DERIVED.<name>" for a value computed by a resolver rather than stored
directly (the two variation-quality slots).

These are initial game-design weights, not formulas from an existing cricket
game (per the brief) - they're kept here as named constants specifically so
they stay easy to retune later without touching the calculation engine.
"""

from Player.ratings.errors import ValidationError

BATTING_WEIGHTS = [
    ("batting.timing", 12),
    ("batting.shotSelection", 12),
    ("batting.defensiveTechnique", 8),
    ("batting.attackingTechnique",   8),
    ("batting.placement", 8),
    ("batting.offside", 5),
    ("batting.legside", 5),
    ("batting.straight", 5),
    ("mentality.composure", 5),
    ("mentality.concentration", 5),
    ("mentality.decisionMaking", 2),
    ("mentality.discipline", 2),
    ("physical.footwork", 10),
    ("physical.strength", 8),
    ("physical.balance", 2),
    ("physical.agility", 1),
    ("physical.runningSpeed", 1),
    ("physical.stamina", 1),
]
# batting.vsSpin/vsPace are NOT weighted in here - calculate_batting_rating
# (calculators.py) applies them afterwards as a blend on top of this weighted
# rating instead (BATTING_VS_BLEND below), and generate_detailed_attributes
# inverts that same blend so the result still reproduces player.batting. Both
# sides import this one constant instead of hardcoding the split twice.
BATTING_VS_BLEND = {"base": 0.8, "vsSpin": 0.10, "vsPace": 0.10}

# Phase 1 has no "wicketkeeping" core stat of its own, so a keeper's
# keeping_level is estimated from batting/fielding instead - used both by
# generate_detailed_attributes (to anchor the real detailed wicketkeeping
# attributes) and by app/game/view.py's Overall approximation for PlayerCard
# (which has no detailed-attribute lookup available). One shared constant so
# those two can't drift apart the way BATTING_VS_BLEND briefly did.
KEEPING_LEVEL_BLEND = {"batting": 0.3, "fielding": 0.7}

PACE_BOWLING_WEIGHTS = [
    ("paceBowling.pace", 10),
    ("paceBowling.lineControl", 12),
    ("paceBowling.lengthControl", 12),
    ("paceBowling.releaseConsistency", 10),
    ("paceBowling.swing", 10),
    ("paceBowling.seam", 10),
    ("paceBowling.bounce", 7),
    ("paceBowling.yorker", 7),
    ("paceBowling.bouncer", 5),
    ("DERIVED.paceVariationQuality", 7),
    ("paceBowling.disguise", 3),
    ("mentality.tacticalAwareness", 3),
    ("mentality.composure", 2),
    ("physical.stamina", 2),
]

SPIN_BOWLING_WEIGHTS = [
    ("spinBowling.turn", 15),
    ("spinBowling.lineControl", 12),
    ("spinBowling.lengthControl", 12),
    ("spinBowling.releaseConsistency", 10),
    ("spinBowling.drift", 8),
    ("spinBowling.dip", 8),
    ("spinBowling.flightControl", 8),
    ("spinBowling.paceVariation", 7),
    ("DERIVED.spinVariationQuality", 8),
    ("spinBowling.disguise", 5),
    ("mentality.tacticalAwareness", 3),
    ("mentality.composure", 2),
    ("physical.stamina", 2),
]

FIELDING_WEIGHTS = [
    ("fielding.catching", 18),
    ("fielding.groundFielding", 15),
    ("fielding.positioning", 8),
    ("fielding.throwAccuracy", 10),
    ("fielding.throwPower", 6),
    ("fielding.pickupAndRelease", 5),
    ("fielding.diving", 3),
    ("fielding.boundaryAwareness", 2),
    ("physical.runningSpeed", 10),  
    ("physical.reflexes", 8),
    ("physical.balance", 2),
    ("physical.agility", 5),
    ("mentality.anticipation", 8),
]

WICKETKEEPING_WEIGHTS = [
    ("wicketkeeping.glovework", 15),
    ("wicketkeeping.byesPrevention", 5),
    ("wicketkeeping.standingUp", 8),
    ("wicketkeeping.standingBack", 8),
    ("wicketkeeping.stumping", 10),
    ("wicketkeeping.legSideCollection", 5),
    ("fielding.diving", 5),  
    ("fielding.catching", 10), 
    ("mentality.concentration", 2),
    ("mentality.anticipation", 8),
    ("mentality.decisionMaking", 3),
    ("physical.footwork", 5), 
    ("physical.balance", 2),
    ("physical.reflexes", 14),
]

MENTALITY_SUMMARY_WEIGHTS = [
    ("mentality.concentration", 20),
    ("mentality.composure", 20),
    ("mentality.decisionMaking", 15),
    ("mentality.tacticalAwareness", 15),
    ("mentality.adaptability", 10),
    ("mentality.discipline", 10),
    ("mentality.resilience", 5),
    ("mentality.gameReading", 5),
]

PHYSICAL_SUMMARY_WEIGHTS = [
    ("physical.strength", 15),
    ("physical.stamina", 15),
    ("physical.runningSpeed", 15),
    ("physical.agility", 15),
    ("physical.reflexes", 15),
    ("physical.footwork", 10),
    ("physical.balance", 10),
    ("physical.recovery", 5),
]

# Role -> {core rating name: weight percent}. Every row totals 100 (section 12).
ROLE_OVERALL_WEIGHTS = {
    "specialistBatter": {"batting": 90, "bowling": 0, "fielding": 10, "wicketkeeping": 0},
    "specialistBowler": {"batting": 5, "bowling": 90, "fielding": 5, "wicketkeeping": 0},
    "battingAllRounder": {"batting": 70, "bowling": 25, "fielding": 5, "wicketkeeping": 0},
    "bowlingAllRounder": {"batting": 25, "bowling": 70, "fielding": 5, "wicketkeeping": 0},
    "balancedAllRounder": {"batting": 48, "bowling": 48, "fielding": 4, "wicketkeeping": 0},
    "wicketkeeperBatter": {"batting": 70, "bowling": 0, "fielding": 0, "wicketkeeping": 30},
}

CORE_WEIGHT_TABLES = {
    "batting": BATTING_WEIGHTS,
    "paceBowling": PACE_BOWLING_WEIGHTS,
    "spinBowling": SPIN_BOWLING_WEIGHTS,
    "fielding": FIELDING_WEIGHTS,
    "wicketkeeping": WICKETKEEPING_WEIGHTS,
    "mentalitySummary": MENTALITY_SUMMARY_WEIGHTS,
    "physicalSummary": PHYSICAL_SUMMARY_WEIGHTS,
}


def validate_weight_table_totals_100(name, table, tolerance=1e-6):
    total = sum(weight for _, weight in table)
    if abs(total - 100) > tolerance:
        raise ValidationError(f"Weight table '{name}' totals {total}, not 100")


def validate_role_weights_total_100(tolerance=1e-6):
    for role, weights in ROLE_OVERALL_WEIGHTS.items():
        total = sum(weights.values())
        if abs(total - 100) > tolerance:
            raise ValidationError(f"Role overall weights for '{role}' total {total}, not 100")


def _validate_batting_vs_blend_totals_1(tolerance=1e-9):
    total = sum(BATTING_VS_BLEND.values())
    if abs(total - 1.0) > tolerance:
        raise ValidationError(f"BATTING_VS_BLEND totals {total}, not 1.0")


def _validate_keeping_level_blend_totals_1(tolerance=1e-9):
    total = sum(KEEPING_LEVEL_BLEND.values())
    if abs(total - 1.0) > tolerance:
        raise ValidationError(f"KEEPING_LEVEL_BLEND totals {total}, not 1.0")


def _self_check():
    for name, table in CORE_WEIGHT_TABLES.items():
        validate_weight_table_totals_100(name, table)
    validate_role_weights_total_100()
    _validate_batting_vs_blend_totals_1()
    _validate_keeping_level_blend_totals_1()


_self_check()
