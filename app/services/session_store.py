"""In-memory game session storage, one running server instance's worth.

A plain dict keyed by session_id. No persistence beyond the process
lifetime, and no locking: fine for the single-player, single-process MVP
this app targets.
"""

from app.game.engine import GameSession

_sessions: dict[str, GameSession] = {}


def save(session: GameSession) -> None:
    _sessions[session.session_id] = session


def get(session_id: str) -> GameSession:
    session = _sessions.get(session_id)
    if session is None:
        raise KeyError(session_id)
    return session
