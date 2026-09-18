"""In-memory player pool storage, mirroring session_store.py."""

from app.game.player_pool import PlayerPool

_pools: dict[str, PlayerPool] = {}


def save(pool: PlayerPool) -> None:
    _pools[pool.pool_id] = pool


def get(pool_id: str) -> PlayerPool:
    pool = _pools.get(pool_id)
    if pool is None:
        raise KeyError(pool_id)
    return pool
