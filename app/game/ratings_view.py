"""Serializes a Player + its Phase 2 DetailedPlayerAttributes into a plain
dict for the player-detail API response. Kept separate from view.py since
this is about the ratings/attributes system, not auction/game state.
"""

from Player.player import Player
from Player.ratings import DetailedPlayerAttributes, RatingResult, calculate_player_ratings
from Player.ratings.weights import BATTING_VS_BLEND, CORE_WEIGHT_TABLES, ROLE_OVERALL_WEIGHTS


def _serialize_rating(result) -> dict:
    if isinstance(result, RatingResult):
        serialized = {"raw": round(result.raw, 2), "displayed": result.displayed, "unavailable": False, "missing": None}
        if result.breakdown:
            serialized["breakdown"] = [
                {"path": path, "value": value, "weight": weight, "contribution": round(contribution, 3)}
                for path, value, weight, contribution in result.breakdown
            ]
        return serialized
    return {"raw": None, "displayed": None, "unavailable": True, "missing": result.missing}


def player_detail(player: Player, detail: DetailedPlayerAttributes) -> dict:
    ratings = calculate_player_ratings(detail)
    return {
        "player_id": player.player_id,
        "name": player.name,
        "position": player.position,
        "role": detail.role,
        "primary_bowling_style": detail.primary_bowling_style,
        "batting_hand": player.batting_hand,
        "batting_order": player.batting_order,
        "nationality": player.nationality,
        "player_type": player.player_type,
        "core": {
            "batting": player.batting,
            "bowling": player.bowling,
            "fielding": player.fielding,
            "estimated_price": player.estimated_price,
        },
        "ratings": {key: _serialize_rating(value) for key, value in ratings.items()},
        "attributes": {
            "batting": detail.batting,
            "paceBowling": detail.paceBowling,
            "spinBowling": detail.spinBowling,
            "fielding": detail.fielding,
            "wicketkeeping": detail.wicketkeeping,
            "physical": detail.physical,
            "mentality": detail.mentality,
            "traits": detail.traits,
            "state": detail.state,
            "repertoire": detail.repertoire,
        },
    }


def preview_ratings(detail: DetailedPlayerAttributes) -> dict:
    """Stateless rating computation for the Create Player / weight-tuning
    tool - breakdown=True so the caller can see exactly how each attribute
    contributed, not just the final number.
    """
    ratings = calculate_player_ratings(detail, breakdown=True)
    return {"ratings": {key: _serialize_rating(value) for key, value in ratings.items()}}


def weight_tables() -> dict:
    return {
        "tables": CORE_WEIGHT_TABLES,
        "role_overall": ROLE_OVERALL_WEIGHTS,
        "batting_vs_blend": BATTING_VS_BLEND,
    }
