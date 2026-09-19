from typing import Optional

from fastapi import APIRouter, HTTPException

from app.game import player_pool, ratings_view, view
from app.schemas.game import GeneratePoolRequest, PoolPlayers, PoolSummary
from app.schemas.ratings import (
    CustomPlayerCreateRequest,
    CustomPlayerPreviewRequest,
    PlayerDetailResponse,
    WeightTablesResponse,
)
from app.services import pool_store
from Player.ratings.model import DetailedPlayerAttributes

router = APIRouter(prefix="/api/players", tags=["players"])


def _get_pool(pool_id: str) -> player_pool.PlayerPool:
    try:
        return pool_store.get(pool_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Player pool not found.")


def _build_detail(body: CustomPlayerPreviewRequest, player_id: int = 0) -> DetailedPlayerAttributes:
    detail = DetailedPlayerAttributes(
        player_id=player_id,
        role=body.role,
        primary_bowling_style=body.primary_bowling_style,
        batting=dict(body.attributes.batting),
        paceBowling=dict(body.attributes.paceBowling),
        spinBowling=dict(body.attributes.spinBowling),
        fielding=dict(body.attributes.fielding),
        wicketkeeping=dict(body.attributes.wicketkeeping),
        physical=dict(body.attributes.physical),
        mentality=dict(body.attributes.mentality),
    )
    # An empty repertoire ({}) means "no available variations, quality 0" -
    # a valid, computable state (section 7) - whereas an absent one means
    # "no repertoire data at all", which is what makes DERIVED.*VariationQuality
    # show up as missing. The Create Player tool doesn't build repertoires, so
    # default to the valid empty state instead of leaving pace/spin bowling
    # permanently unavailable.
    if detail.paceBowling:
        detail.repertoire.setdefault("pace", {})
    if detail.spinBowling:
        detail.repertoire.setdefault("spin", {})
    return detail


@router.get("/weight-tables", response_model=WeightTablesResponse)
async def get_weight_tables():
    return ratings_view.weight_tables()


@router.post("/preview")
async def preview_custom_player(body: CustomPlayerPreviewRequest):
    detail = _build_detail(body)
    return ratings_view.preview_ratings(detail)


@router.post("/generate", response_model=PoolSummary)
async def generate_pool(body: Optional[GeneratePoolRequest] = None):
    seed = body.seed if body else None
    count = (body.count if body and body.count else None) or player_pool.DEFAULT_POOL_SIZE
    international_count = (body.international_count if body and body.international_count else None) or 0
    pool = player_pool.create_pool(seed=seed, count=count, international_count=international_count)
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


@router.post("/{pool_id}/shortlist/{player_id}", response_model=PoolSummary)
async def toggle_pool_shortlist(pool_id: str, player_id: int):
    pool = _get_pool(pool_id)
    player_pool.toggle_shortlist(pool, player_id)
    return view.pool_summary(pool)


@router.post("/{pool_id}/custom", response_model=PlayerDetailResponse)
async def create_custom_player(pool_id: str, body: CustomPlayerCreateRequest):
    pool = _get_pool(pool_id)
    detail = _build_detail(body)
    player = player_pool.add_custom_player(
        pool,
        detail,
        name=body.name,
        position=body.position,
        batting_hand=body.batting_hand,
        bowling_type=body.bowling_type,
        batting_order=body.batting_order,
        fame=body.fame,
        player_type=body.player_type,
    )
    return ratings_view.player_detail(player, detail)
