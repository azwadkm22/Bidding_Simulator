"""Serializes a GameSession into plain dicts for API responses.

Kept separate from engine.py so the engine has no knowledge of the API/response
shape, and no print()/input() is involved anywhere in this path.
"""

from Player.player import Player
from Team.starting_eleven import StartingEleven

from app.game.engine import (
    ALLOWED_INCREMENTS,
    DECIDED_PHASES,
    OPEN_PHASES,
    BidderHandle,
    GameSession,
)
from app.game.player_pool import PlayerPool

MIN_PLAYERS_FOR_STARTING_ELEVEN = 11


def serialize(session: GameSession) -> dict:
    return {
        "session_id": session.session_id,
        "seed": session.seed,
        "pool_id": session.pool_id,
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
        "deal_grade": getattr(player, "deal_grade", None),
    }


def team_detail(handle: BidderHandle) -> dict:
    return _bidder_summary(handle, detailed=True)


def starting_eleven_detail(handle: BidderHandle) -> dict:
    team = handle.team
    base = {"key": handle.key, "name": handle.display_name}

    if team.number_of_players < MIN_PLAYERS_FOR_STARTING_ELEVEN:
        return {
            **base,
            "available": False,
            "reason": f"Needs at least {MIN_PLAYERS_FOR_STARTING_ELEVEN} players in the squad "
            f"(has {team.number_of_players}).",
            "lineup": [],
            "bench": [],
            "batting_rating": None,
            "bowling_rating": None,
            "fielding_rating": None,
        }

    try:
        builder = StartingEleven()
        lineup = builder.create_starting_eleven(team)
        if len(lineup) < MIN_PLAYERS_FOR_STARTING_ELEVEN:
            raise ValueError("Squad composition can't fill a full lineup yet.")
        bench_ids = set(builder.print_bench())
        bench_players = [p for p in team.player_list if p.player_id in bench_ids]
        return {
            **base,
            "available": True,
            "reason": None,
            "lineup": [_player_card(p) for p in lineup],
            "bench": [_player_card(p) for p in bench_players],
            "batting_rating": builder.evaluate_batting(),
            "bowling_rating": builder.evaluate_bowling(),
            "fielding_rating": builder.evaluate_fielding(),
        }
    except (ZeroDivisionError, IndexError, ValueError):
        # create_starting_eleven's picking algorithm assumes a reasonably
        # balanced squad (e.g. at least one bowler-type player); an unusual
        # squad shape can still fall short of that even past the player-count
        # floor above, so this is a real (if rare) outcome, not a bug to chase.
        return {
            **base,
            "available": False,
            "reason": "Squad isn't balanced enough yet to form a full starting XI.",
            "lineup": [],
            "bench": [],
            "batting_rating": None,
            "bowling_rating": None,
            "fielding_rating": None,
        }


def game_summary(session: GameSession) -> dict:
    sold_players = []
    for handle in session.all_handles():
        for player in handle.team.player_list:
            entry = _player_card(player)
            entry["buyer"] = handle.display_name
            entry["buyer_key"] = handle.key
            entry["is_user"] = handle.is_user
            sold_players.append(entry)
    sold_players.sort(key=lambda p: p["selling_price"] or 0, reverse=True)

    teams = []
    for handle in session.all_handles():
        team_entry = _bidder_summary(handle, detailed=False)
        team_entry["is_user"] = handle.is_user
        team_entry["starting_eleven"] = starting_eleven_detail(handle)
        teams.append(team_entry)

    return {
        "sold_players": sold_players,
        "unsold_count": len(session.unsold_this_round),
        "teams": teams,
    }


def pool_summary(pool: PlayerPool) -> dict:
    gen = pool.generation

    position_counts: dict = {}
    bowling_type_counts = {"Pacer": 0, "Spinner": 0}
    for player in gen.list_of_players:
        position_counts[player.position] = position_counts.get(player.position, 0) + 1
        if player.position in ("Bowler", "Allrounder"):
            bowling_type_counts[player.bowling_type] = bowling_type_counts.get(player.bowling_type, 0) + 1

    return {
        "pool_id": pool.pool_id,
        "seed": pool.seed,
        "count": pool.count,
        "position_counts": position_counts,
        "bowling_type_counts": bowling_type_counts,
        "players_above_80": len(gen.players_above_80),
        "players_above_90": len(gen.players_above_90),
        "top_batsmen": [_player_card(p) for p in gen.top_ten_batsmen],
        "top_bowlers": [_player_card(p) for p in gen.top_ten_bowlers],
        "top_allrounders": [_player_card(p) for p in gen.top_ten_allrounders],
        "top_wicketkeepers": [_player_card(p) for p in gen.top_eight_wicketkeepers],
        "top_openers": [_player_card(p) for p in gen.top_ten_openers],
        "top_pacers": [_player_card(p) for p in gen.top_ten_pacers],
        "top_spinners": [_player_card(p) for p in gen.top_ten_spinners],
        "most_expensive": [_player_card(p) for p in gen.top_ten_most_expensive],
    }


def pool_players(pool: PlayerPool) -> dict:
    players = pool.generation.list_of_players
    return {"count": len(players), "players": [_player_card(p) for p in players]}


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
