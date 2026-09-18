"""Player pool generation, isolated from starting an auction.

A PlayerPool is generated once - optionally with a seed for reproducibility -
and can be reused to start any number of independent auctions afterward.
Each auction gets its own fresh Player objects reconstructed from a snapshot
taken at pool-creation time, so playing an auction (which mutates
selling_price/deal_grade on the Player objects) never corrupts the pool for a
later reuse, and starting a second auction from the same pool doesn't show
players as already sold from the first one.
"""

import random
import uuid
from dataclasses import dataclass, field
from typing import Optional

from Player.generate_players import get_list_of_players
from Player.player import Player
from Player.player_generation_stats import PlayerGenStat
from Player.ratings.generation import generate_detailed_attributes

DEFAULT_POOL_SIZE = 250
SEED_MAX = 2**31 - 1


@dataclass
class PlayerPool:
    pool_id: str
    seed: int
    count: int
    generation: PlayerGenStat  # read-only for display; never touched by an auction
    snapshot: list = field(default_factory=list)  # [(player_id, json_data), ...] pristine copy
    # Phase 2: player_id -> DetailedPlayerAttributes, keyed separately from
    # Player objects since detail isn't part of the Player class itself (see
    # Player/ratings/). Generated once per pool and immutable afterward - an
    # auction reconstructs fresh Player objects per instantiate_players(),
    # but the detailed breakdown behind each player_id stays the same no
    # matter how many auctions this pool is reused for.
    detailed: dict = field(default_factory=dict)


def create_pool(seed: Optional[int] = None, count: int = DEFAULT_POOL_SIZE) -> PlayerPool:
    """Generates a fresh player pool, reseeding the process-wide random module
    first so a given seed reliably reproduces the same players.

    Same caveat as engine.create_game: this reseeds the *global* random
    module (no domain code accepts an injectable RNG), so generating a new
    seeded pool while another session's live clock is ticking in the
    background will perturb that session's randomness too.

    Phase 2 (detailed attributes, see Player/ratings/generation.py) runs
    immediately after Phase 1 here, continuing the same seeded `random`
    stream rather than reseeding again - so "the same seed" really does
    drive one continuous, reproducible generation of both layers together.
    """
    if seed is None:
        seed = random.randint(0, SEED_MAX)
    random.seed(seed)

    players = get_list_of_players(count)
    players = sorted(players, key=lambda p: p.estimated_price, reverse=True)
    generation = PlayerGenStat(players)
    snapshot = [(p.player_id, p.get_JSON_data()) for p in players]
    detailed = {p.player_id: generate_detailed_attributes(p) for p in players}

    return PlayerPool(
        pool_id=str(uuid.uuid4()),
        seed=seed,
        count=count,
        generation=generation,
        snapshot=snapshot,
        detailed=detailed,
    )


def instantiate_players(pool: PlayerPool) -> list:
    """Fresh Player objects from the pool's pristine snapshot, in the same
    price-sorted order the pool was generated in - safe to hand to a new
    auction even if the pool has already been used by a previous one.
    """
    return [Player(player_id=player_id, json_data=dict(data)) for player_id, data in pool.snapshot]
