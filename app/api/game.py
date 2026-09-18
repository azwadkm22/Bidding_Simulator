from fastapi import APIRouter, HTTPException

from app.game import engine, view
from typing import Optional

from app.schemas.game import (
    BidderSummary,
    BidRequest,
    GameState,
    GameSummary,
    NewGameRequest,
    RemainingPlayers,
    StartingElevenResponse,
)
from app.services import live_clock, pool_store, session_store

router = APIRouter(prefix="/api/game", tags=["game"])


def _get_session(session_id: str) -> engine.GameSession:
    try:
        return session_store.get(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Game session not found.")


# Every route below is `async def`, even where nothing is awaited: this keeps
# it on the single asyncio event loop thread (instead of FastAPI's worker
# threadpool for plain `def` routes), so a request can never interleave
# mid-mutation with the background live_clock tick. See services/live_clock.py.


@router.post("/new", response_model=GameState)
async def new_game(body: Optional[NewGameRequest] = None):
    pool = None
    seed = None
    if body and body.pool_id:
        try:
            pool = pool_store.get(body.pool_id)
        except KeyError:
            raise HTTPException(status_code=404, detail="Player pool not found.")
    elif body:
        seed = body.seed

    session = engine.create_game(seed=seed, player_pool=pool)
    session_store.save(session)
    live_clock.start(session)
    return view.serialize(session)


@router.get("/{session_id}", response_model=GameState)
async def get_game(session_id: str):
    session = _get_session(session_id)
    return view.serialize(session)


@router.get("/{session_id}/teams/{team_key}", response_model=BidderSummary)
async def get_team(session_id: str, team_key: str):
    session = _get_session(session_id)
    handle = session.find_handle(team_key)
    if handle is None:
        raise HTTPException(status_code=404, detail="Team not found.")
    return view.team_detail(handle)


@router.get("/{session_id}/teams/{team_key}/starting-eleven", response_model=StartingElevenResponse)
async def get_starting_eleven(session_id: str, team_key: str):
    session = _get_session(session_id)
    handle = session.find_handle(team_key)
    if handle is None:
        raise HTTPException(status_code=404, detail="Team not found.")
    return view.starting_eleven_detail(handle)


@router.get("/{session_id}/summary", response_model=GameSummary)
async def get_summary(session_id: str):
    session = _get_session(session_id)
    return view.game_summary(session)


@router.get("/{session_id}/players/remaining", response_model=RemainingPlayers)
async def get_remaining_players(session_id: str):
    session = _get_session(session_id)
    return view.remaining_players(session)


@router.post("/{session_id}/bid", response_model=GameState)
async def bid(session_id: str, body: BidRequest):
    session = _get_session(session_id)
    try:
        engine.process_bid(session, body.increment)
    except engine.InvalidBidError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return view.serialize(session)


@router.post("/{session_id}/pass", response_model=GameState)
async def pass_turn(session_id: str):
    session = _get_session(session_id)
    try:
        engine.process_pass(session)
    except engine.InvalidBidError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return view.serialize(session)


@router.post("/{session_id}/skip", response_model=GameState)
async def skip(session_id: str):
    session = _get_session(session_id)
    try:
        engine.skip_to_outcome(session)
    except engine.InvalidBidError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return view.serialize(session)


@router.post("/{session_id}/complete-simulation", response_model=GameState)
async def complete_simulation(session_id: str):
    session = _get_session(session_id)
    engine.complete_simulation(session)
    return view.serialize(session)


@router.post("/{session_id}/advance", response_model=GameState)
async def advance(session_id: str):
    session = _get_session(session_id)
    try:
        engine.advance(session)
    except engine.InvalidBidError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return view.serialize(session)


@router.post("/{session_id}/pause", response_model=GameState)
async def pause(session_id: str):
    session = _get_session(session_id)
    engine.pause(session)
    return view.serialize(session)


@router.post("/{session_id}/resume", response_model=GameState)
async def resume(session_id: str):
    session = _get_session(session_id)
    engine.resume(session)
    return view.serialize(session)
