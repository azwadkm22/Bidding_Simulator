"""Serializes a GameSession into plain dicts for API responses.

Kept separate from engine.py so the engine has no knowledge of the API/response
shape, and no print()/input() is involved anywhere in this path.
"""

from Player.player import Player

from app.game.engine import (
    ALLOWED_INCREMENTS,
    DECIDED_PHASES,
    OPEN_PHASES,
    BidderHandle,
    GameSession,
)


def serialize(session: GameSession) -> dict:
    return {
        "session_id": session.session_id,
        "phase": session.phase.value,
        "paused": session.paused,
        "round_number": session.round_number,
        "players_remaining": len(session.queue) + len(session.unsold_this_round),
        "current_player": _player_card(session.current_player) if session.current_player else None,
        "current_price": session.current_price,
        "current_leader": session.current_leader.display_name if session.current_leader else None,
        "available_actions": _available_actions(session),
        "last_result": session.last_result,
        "allowed_increments": ALLOWED_INCREMENTS,
        "user": _bidder_summary(session.user_handle, detailed=True),
        "rivals": [_bidder_summary(h) for h in session.bot_handles],
        "event_log": session.event_log,
    }


def _available_actions(session: GameSession) -> list:
    if session.phase in OPEN_PHASES:
        return ["bid", "pass", "skip"]
    if session.phase in DECIDED_PHASES:
        return ["advance"]
    return []


def _player_card(player: Player) -> dict:
    return {
        "player_id": player.player_id,
        "name": player.name,
        "position": player.position,
        "batting": player.batting,
        "bowling": player.bowling,
        "fielding": player.fielding,
        "batting_hand": player.batting_hand,
        "batting_order": player.batting_order,
        "bowling_type": player.bowling_type,
        "bowling_style": player.bowling_style,
        "estimated_price": player.estimated_price,
        "selling_price": player.selling_price or None,
    }


def team_detail(handle: BidderHandle) -> dict:
    return _bidder_summary(handle, detailed=True)


def remaining_players(session: GameSession) -> dict:
    players = list(session.queue) + session.unsold_this_round
    players.sort(key=lambda p: p.estimated_price, reverse=True)
    return {
        "count": len(players),
        "players": [_player_card(p) for p in players],
    }


def _bidder_summary(handle: BidderHandle, detailed: bool = False) -> dict:
    team = handle.team
    summary = {
        "key": handle.key,
        "name": handle.display_name,
        "budget": handle.bidder.budget,
        "squad_size": team.number_of_players,
    }
    if detailed:
        summary["squad"] = [_player_card(p) for p in team.player_list]
        summary["composition"] = {
            "batsmen": team.number_of_batsmen,
            "bowlers": team.number_of_bowlers,
            "allrounders": team.number_of_allrounders,
            "wicketkeepers": team.number_of_wicketkeepers,
        }
    return summary
