from typing import Optional

from fastapi import APIRouter, HTTPException

from app.game import player_pool, ratings_view, view
from app.schemas.game import GeneratePoolRequest, PoolPlayers, PoolSummary
from app.schemas.ratings import PlayerDetailResponse
from app.services import pool_store

router = APIRouter(prefix="/api/players", tags=["players"])


def _get_pool(pool_id: str) -> player_pool.PlayerPool:
    try:
        return pool_store.get(pool_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Player pool not found.")


@router.post("/generate", response_model=PoolSummary)
async def generate_pool(body: Optional[GeneratePoolRequest] = None):
    seed = body.seed if body else None
    count = (body.count if body and body.count else None) or player_pool.DEFAULT_POOL_SIZE
    pool = player_pool.create_pool(seed=seed, count=count)
    pool_store.save(pool)
    return view.pool_summary(pool)


@router.get("/{pool_id}/summary", response_model=PoolSummary)
async def get_pool_summary(pool_id: str):
    pool = _get_pool(pool_id)
    return view.pool_summary(pool)


@router.get("/{pool_id}/players", response_model=PoolPlayers)
async def get_pool_players(pool_id: str):
    pool = _get_pool(pool_id)
    return view.pool_players(pool)


@router.get("/{pool_id}/players/{player_id}/detail", response_model=PlayerDetailResponse)
async def get_player_detail(pool_id: str, player_id: int):
    pool = _get_pool(pool_id)
    player = next((p for p in pool.generation.list_of_players if p.player_id == player_id), None)
    if player is None:
        raise HTTPException(status_code=404, detail="Player not found in this pool.")
    detail = pool.detailed.get(player_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="No detailed attributes available for this player.")
    return ratings_view.player_detail(player, detail)
