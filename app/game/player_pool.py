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
from Player.ratings import DetailedPlayerAttributes, RatingResult, calculate_player_ratings
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
    # The human user's own pre-auction shortlist (player_ids) - built while
    # browsing the pool, before any GameSession exists. Copied into
    # GameSession.user_shortlist when an auction starts from this pool (see
    # engine.create_game), then freely editable there independently - editing
    # it mid-auction does not write back to the pool.
    user_shortlist: set = field(default_factory=set)


def toggle_shortlist(pool: PlayerPool, player_id: int) -> bool:
    """Adds/removes a player from the pool's pre-auction shortlist. Returns
    the new membership state (True = now shortlisted). Mirrors
    engine.toggle_shortlist's semantics for the in-auction version.
    """
    if player_id in pool.user_shortlist:
        pool.user_shortlist.discard(player_id)
        return False
    pool.user_shortlist.add(player_id)
    return True


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


def add_custom_player(
    pool: PlayerPool,
    detail: DetailedPlayerAttributes,
    name: str,
    position: str,
    batting_hand: str,
    bowling_type: str,
    batting_order: str,
    fame: int,
) -> Player:
    """Hand-built player for the Create Player / weight-tuning tool: batting/
    bowling/fielding core stats are derived from the detailed attributes
    (via calculate_player_ratings) instead of Phase 1's random generation, so
    what you see in the attribute editor is exactly what ends up on the
    player. Mutates `pool` in place (list_of_players, generation, snapshot,
    detailed) - the caller is expected to already hold the stored pool
    instance (see pool_store.get), not a copy.
    """
    new_id = max((p.player_id for p in pool.generation.list_of_players), default=0) + 1

    ratings = calculate_player_ratings(detail)

    def _core(key: str, fallback: int = 50) -> int:
        result = ratings.get(key)
        return result.displayed if isinstance(result, RatingResult) else fallback

    bowling_key = "paceBowling" if bowling_type == "Pacer" else "spinBowling"
    json_data = {
        "name": name,
        "batting": _core("batting"),
        "bowling": _core(bowling_key),
        "fielding": _core("fielding"),
        "position": position,
        "fame": fame,
        "estimated_price": 1,
        "batting_hand": batting_hand,
        "bowling_type": bowling_type,
        "bowling_style": "Medium" if bowling_type == "Pacer" else "Off-Spin",
        "batting_order": batting_order,
        "selling_price": 0,
    }
    player = Player(player_id=new_id, json_data=json_data)
    player.estimated_price = player.getEstimatedPrice()

    detail.player_id = new_id
    pool.generation.list_of_players.append(player)
    pool.generation = PlayerGenStat(pool.generation.list_of_players)
    pool.snapshot.append((new_id, player.get_JSON_data()))
    pool.detailed[new_id] = detail
    pool.count += 1

    return player
