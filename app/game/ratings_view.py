"""Serializes a Player + its Phase 2 DetailedPlayerAttributes into a plain
dict for the player-detail API response. Kept separate from view.py since
this is about the ratings/attributes system, not auction/game state.
"""

from Player.player import Player
from Player.ratings import DetailedPlayerAttributes, RatingResult, calculate_player_ratings


def _serialize_rating(result) -> dict:
    if isinstance(result, RatingResult):
        return {"raw": round(result.raw, 2), "displayed": result.displayed, "unavailable": False, "missing": None}
    return {"raw": None, "displayed": None, "unavailable": True, "missing": result.missing}


def player_detail(player: Player, detail: DetailedPlayerAttributes) -> dict:
    ratings = calculate_player_ratings(detail)
    return {
        "player_id": player.player_id,
        "name": player.name,
        "position": player.position,
        "role": detail.role,
        "primary_bowling_style": detail.primary_bowling_style,
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
