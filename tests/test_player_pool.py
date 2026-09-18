from app.game import player_pool
from app.game.engine import create_game


def test_same_seed_reproduces_the_same_pool():
    pool_a = player_pool.create_pool(seed=555, count=20)
    pool_b = player_pool.create_pool(seed=555, count=20)

    names_a = [p.name for p in pool_a.generation.list_of_players]
    names_b = [p.name for p in pool_b.generation.list_of_players]
    assert names_a == names_b
    assert pool_a.pool_id != pool_b.pool_id  # distinct pools, same contents


def test_different_seeds_produce_different_pools():
    pool_a = player_pool.create_pool(seed=1, count=20)
    pool_b = player_pool.create_pool(seed=2, count=20)

    names_a = [p.name for p in pool_a.generation.list_of_players]
    names_b = [p.name for p in pool_b.generation.list_of_players]
    assert names_a != names_b


def test_no_seed_still_reports_a_usable_seed():
    pool = player_pool.create_pool(count=10)
    assert isinstance(pool.seed, int)

    replay = player_pool.create_pool(seed=pool.seed, count=10)
    names_original = [p.name for p in pool.generation.list_of_players]
    names_replay = [p.name for p in replay.generation.list_of_players]
    assert names_original == names_replay


def test_instantiate_players_gives_fresh_unsold_copies():
    pool = player_pool.create_pool(seed=42, count=10)

    first_batch = player_pool.instantiate_players(pool)
    first_batch[0].setSellingPrice(999)
    first_batch[0].deal_grade = "A"

    second_batch = player_pool.instantiate_players(pool)

    assert second_batch[0].selling_price == 0
    assert getattr(second_batch[0], "deal_grade", None) is None
    # Same underlying stats/order, just independent objects.
    assert [p.name for p in first_batch] == [p.name for p in second_batch]
    assert first_batch[0] is not second_batch[0]


def test_reusing_a_pool_across_two_auctions_stays_isolated():
    pool = player_pool.create_pool(seed=7, count=30)

    session_a = create_game(player_pool=pool)
    session_a.current_player.setSellingPrice(500)

    session_b = create_game(player_pool=pool)

    assert session_a.seed == session_b.seed == pool.seed
    # session_b's queue must not show session_a's mutation.
    assert all(p.selling_price == 0 for p in session_b.queue)
    assert session_a.current_player is not session_b.current_player
