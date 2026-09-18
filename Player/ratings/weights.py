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
    ("batting.timing", 15),
    ("batting.shotSelection", 12),
    ("batting.footwork", 10),
    ("batting.defensiveTechnique", 10),
    ("batting.attackingTechnique", 10),
    ("batting.placement", 8),
    ("batting.power", 8),
    ("batting.offside", 5),
    ("batting.legside", 5),
    ("batting.straight", 5),
    ("mentality.composure", 5),
    ("mentality.concentration", 5),
    ("batting.runningBetweenWickets", 2),
]

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
    ("fielding.catching", 20),
    ("fielding.groundFielding", 15),
    ("fielding.positioning", 8),
    ("mentality.anticipation", 8),
    ("physical.reflexes", 8),
    ("fielding.throwAccuracy", 10),
    ("fielding.throwPower", 6),
    ("fielding.pickupAndRelease", 5),
    ("physical.runningSpeed", 6),
    ("physical.acceleration", 4),
    ("physical.agility", 5),
    ("fielding.diving", 3),
    ("fielding.boundaryAwareness", 2),
]

WICKETKEEPING_WEIGHTS = [
    ("wicketkeeping.glovework", 20),
    ("wicketkeeping.footwork", 12),
    ("physical.reflexes", 12),
    ("mentality.anticipation", 8),
    ("wicketkeeping.standingUp", 10),
    ("wicketkeeping.standingBack", 8),
    ("wicketkeeping.stumping", 10),
    ("wicketkeeping.legSideCollection", 5),
    ("wicketkeeping.divingReach", 5),
    ("wicketkeeping.byesPrevention", 5),
    ("wicketkeeping.throwCollection", 3),
    ("mentality.concentration", 2),
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

# Role -> {core rating name: weight percent}. Every row totals 100 (section 12).
ROLE_OVERALL_WEIGHTS = {
    "specialistBatter": {"batting": 85, "bowling": 0, "fielding": 15, "wicketkeeping": 0},
    "specialistBowler": {"batting": 10, "bowling": 80, "fielding": 10, "wicketkeeping": 0},
    "battingAllRounder": {"batting": 60, "bowling": 30, "fielding": 10, "wicketkeeping": 0},
    "bowlingAllRounder": {"batting": 30, "bowling": 60, "fielding": 10, "wicketkeeping": 0},
    "balancedAllRounder": {"batting": 45, "bowling": 45, "fielding": 10, "wicketkeeping": 0},
    "wicketkeeperBatter": {"batting": 55, "bowling": 0, "fielding": 0, "wicketkeeping": 45},
}

CORE_WEIGHT_TABLES = {
    "batting": BATTING_WEIGHTS,
    "paceBowling": PACE_BOWLING_WEIGHTS,
    "spinBowling": SPIN_BOWLING_WEIGHTS,
    "fielding": FIELDING_WEIGHTS,
    "wicketkeeping": WICKETKEEPING_WEIGHTS,
    "mentalitySummary": MENTALITY_SUMMARY_WEIGHTS,
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


def _self_check():
    for name, table in CORE_WEIGHT_TABLES.items():
        validate_weight_table_totals_100(name, table)
    validate_role_weights_total_100()


_self_check()
