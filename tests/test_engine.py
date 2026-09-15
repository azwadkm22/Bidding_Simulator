import random

import pytest

from app.game import engine
from app.game.engine import AuctionPhase, InvalidBidError
from tests.conftest import make_handle, make_player, make_session


def test_valid_human_bid_becomes_leader():
    session = make_session(user_budget=1000)
    engine.process_bid(session, 10)

    assert session.current_leader is session.user_handle
    assert session.current_price == 20
    assert session.phase == AuctionPhase.GOING_ONCE


@pytest.mark.parametrize("bad_amount", [0, -5, -1])
def test_invalid_human_bid_rejected(bad_amount):
    session = make_session(user_budget=1000)

    with pytest.raises(InvalidBidError):
        engine.process_bid(session, bad_amount)

    assert session.current_leader is None
    assert session.current_price == 10


def test_over_budget_bid_rejected():
    session = make_session(user_budget=15)  # current price 10, budget only covers +5

    with pytest.raises(InvalidBidError):
        engine.process_bid(session, 10)

    assert session.current_leader is None
    assert session.user_handle.bidder.budget == 15


def test_bot_bid_acceptance_and_rejection_uses_the_same_price_it_evaluated():
    accept_calls = []
    reject_calls = []

    def accept(player, price):
        accept_calls.append(price)
        return 1

    def reject(player, price):
        reject_calls.append(price)
        return 0

    bot_accept = make_handle("bot-accept", budget=10000, place_bid_result=accept)
    bot_reject = make_handle("bot-reject", budget=10000, place_bid_result=reject)
    session = make_session(bot_handles=[bot_accept, bot_reject])

    engine.process_pass(session)

    assert session.current_leader is bot_accept
    assert len(accept_calls) == 1
    # The price the bot evaluated must be exactly the price it ends up paying.
    assert session.current_price == accept_calls[-1]
    assert len(reject_calls) == 1
    assert bot_reject is not session.current_leader


def test_bot_round_is_simultaneous_not_cascading():
    """Every bot must evaluate the same starting price, not one already bumped
    by an earlier bot in the same round - otherwise bots would effectively see
    each other's moves within a single "instant", which isn't simultaneous."""
    calls = []

    def always_accept(player, price):
        calls.append(price)
        return 1

    bots = [make_handle(f"bot-{i}", budget=10000, place_bid_result=always_accept) for i in range(5)]
    session = make_session(bot_handles=bots)
    base_price = session.current_price
    expected_choices = engine._bot_increment_choices(base_price, session.current_player.estimated_price)

    engine.process_pass(session)

    assert len(calls) == 5
    # If a bot's evaluated price reflected an earlier bot's bid in the same
    # round, some call would exceed base_price + the largest single increment.
    assert max(calls) <= base_price + max(expected_choices)
    assert min(calls) >= base_price + min(expected_choices)

    # Exactly one bid is applied per round, and it's the highest offer.
    assert session.current_price == max(calls)
    assert session.current_leader in bots


def test_sold_flow_settles_atomically():
    winner = make_handle("bot-winner", budget=1000)
    session = make_session(bot_handles=[winner])
    player = session.current_player

    # Simulate the winner having just bid: they lead at price 20.
    session.current_leader = winner
    session.current_price = 20
    session.phase = AuctionPhase.GOING_ONCE

    for _ in range(engine.SILENT_ROUNDS_TO_SOLD):
        engine.process_pass(session)

    assert session.phase == AuctionPhase.SOLD
    assert session.last_result["type"] == "sold"
    assert player.selling_price == 20
    assert player in winner.team.player_list
    assert winner.bidder.budget == 1000 - 20


def test_unsold_flow_when_nobody_ever_bids():
    session = make_session(bot_handles=[make_handle("bot-1"), make_handle("bot-2")])
    player = session.current_player

    for _ in range(engine.SILENT_ROUNDS_TO_UNSOLD):
        engine.process_pass(session)

    assert session.phase == AuctionPhase.UNSOLD
    assert session.last_result["type"] == "unsold"
    assert player in session.unsold_this_round
    assert player.selling_price == 0


def test_no_double_sale_or_action_after_settlement():
    winner = make_handle("bot-winner", budget=1000)
    session = make_session(bot_handles=[winner])
    session.current_leader = winner
    session.current_price = 20
    for _ in range(engine.SILENT_ROUNDS_TO_SOLD):
        engine.process_pass(session)
    assert session.phase == AuctionPhase.SOLD

    # Further bid/pass on an already-decided player must be rejected, not
    # silently re-settle or double-charge.
    with pytest.raises(InvalidBidError):
        engine.process_bid(session, 5)
    with pytest.raises(InvalidBidError):
        engine.process_pass(session)

    # advance() before the outcome is decided must also be rejected.
    fresh = make_session()
    with pytest.raises(InvalidBidError):
        engine.advance(fresh)


def test_opening_round_edge_case_is_fixed():
    """A human bid on what would have been the final silent round must be
    applied, not discarded in favor of marking the player unsold.

    This reproduces the original bidding_simulation.py control-flow bug: `run`
    (silent-round counter) could tip past its unsold threshold in the same
    iteration a valid human bid was collected, discarding that bid. Here we
    pre-set silent_rounds to one below the unsold threshold, then have the
    human bid on that exact round.
    """
    session = make_session(user_budget=1000)
    session.silent_rounds = engine.SILENT_ROUNDS_TO_UNSOLD - 1

    engine.process_bid(session, 10)

    assert session.phase != AuctionPhase.UNSOLD
    assert session.current_leader is session.user_handle
    assert session.current_price == 20
    assert session.silent_rounds == 0


def test_skip_to_outcome_resolves_instantly_without_waiting_on_rounds():
    always_accept = make_handle("bot-1", budget=10000, place_bid_result=1)
    never_accept = make_handle("bot-2", budget=10000, place_bid_result=0)
    session = make_session(bot_handles=[always_accept, never_accept])
    player = session.current_player

    engine.skip_to_outcome(session)

    # bot-1 always accepts, so it wins the player; nothing here waits for the
    # SILENT_ROUNDS_TO_SOLD threshold across separate process_pass calls.
    assert session.phase == AuctionPhase.SOLD
    assert player in always_accept.team.player_list


def test_skip_to_outcome_can_end_in_unsold():
    session = make_session(bot_handles=[make_handle("bot-1"), make_handle("bot-2")])
    player = session.current_player

    engine.skip_to_outcome(session)

    assert session.phase == AuctionPhase.UNSOLD
    assert player in session.unsold_this_round


def test_skip_to_outcome_rejects_when_not_open():
    winner = make_handle("bot-winner", budget=1000)
    session = make_session(bot_handles=[winner])
    session.current_leader = winner
    session.current_price = 20
    for _ in range(engine.SILENT_ROUNDS_TO_SOLD):
        engine.process_pass(session)
    assert session.phase == AuctionPhase.SOLD

    with pytest.raises(InvalidBidError):
        engine.skip_to_outcome(session)


def test_deal_grade_a_for_cheap_and_needed_player():
    winner = make_handle("bot-winner", budget=1000)  # empty squad -> genuinely needs a keeper
    wk_player = make_player(player_id=5, name="WK Star", estimated_price=100, position="Wicketkeeper")
    session = make_session(player=wk_player, bot_handles=[winner])
    session.current_leader = winner
    session.current_price = 20  # well below estimated value -> a clear bargain

    for _ in range(engine.SILENT_ROUNDS_TO_SOLD):
        engine.process_pass(session)

    assert session.phase == AuctionPhase.SOLD
    assert wk_player.deal_grade == "A"
    assert session.last_result["deal_grade"] == "A"


def test_deal_grade_d_for_bad_overpay():
    winner = make_handle("bot-winner", budget=100000)
    player = make_player(player_id=6, name="Overpriced Guy", estimated_price=100, position="Batsmen")
    session = make_session(player=player, bot_handles=[winner])
    session.current_leader = winner
    session.current_price = 500  # far above estimated value regardless of squad need

    for _ in range(engine.SILENT_ROUNDS_TO_SOLD):
        engine.process_pass(session)

    assert player.deal_grade == "D"


def test_weak_player_desperation_bid_is_damped_but_strong_player_is_not():
    """UtilityBasedBidder.calculate_utility gives every bot a flat "need
    bodies" bonus (slot_left_ut/remaining_ut) whenever its squad has open
    slots, regardless of the specific player's own quality. Without damping
    this makes even a weak player attract bids from almost every empty-squad
    bot, driving the price up no matter how low the player's attributes are.
    _bot_wants_to_bid should suppress that for weak players while leaving a
    strong player's acceptance rate essentially unchanged.
    """
    from Bidders.utility_based_bidder import UtilityBasedBidder
    from Team.generate_teams import generate_teams

    weak = make_player(player_id=90, name="Weak", estimated_price=40, position="Batsmen")
    weak.batting = 35
    strong = make_player(player_id=91, name="Strong", estimated_price=180, position="Batsmen")
    strong.batting = 92

    def empty_squad_handle():
        team = generate_teams(1)[0]
        shortlist = type("ShortList", (), {"players": set()})()
        bidder = UtilityBasedBidder("Test Team", "Safe", 2000, team, [], shortlist, [])
        handle = make_handle("bot", budget=2000)
        handle.team = team
        handle.bidder = bidder
        bidder.team = team
        return handle

    trials = 3000
    weak_handle = empty_squad_handle()
    weak_rate = sum(engine._bot_wants_to_bid(weak_handle, weak, 40) for _ in range(trials)) / trials

    strong_handle = empty_squad_handle()
    strong_rate = sum(engine._bot_wants_to_bid(strong_handle, strong, 100) for _ in range(trials)) / trials

    assert weak_rate < 0.05
    assert strong_rate > 0.10


def test_same_seed_reproduces_the_same_player_pool_and_teams():
    session_a = engine.create_game(seed=12345)
    session_b = engine.create_game(seed=12345)

    assert session_a.seed == session_b.seed == 12345
    names_a = [p.name for p in session_a.player_generation.list_of_players]
    names_b = [p.name for p in session_b.player_generation.list_of_players]
    assert names_a == names_b
    prices_a = [p.estimated_price for p in session_a.player_generation.list_of_players]
    prices_b = [p.estimated_price for p in session_b.player_generation.list_of_players]
    assert prices_a == prices_b
    assert [h.display_name for h in session_a.bot_handles] == [h.display_name for h in session_b.bot_handles]


def test_different_seeds_produce_different_pools():
    session_a = engine.create_game(seed=1)
    session_b = engine.create_game(seed=2)

    names_a = [p.name for p in session_a.player_generation.list_of_players]
    names_b = [p.name for p in session_b.player_generation.list_of_players]
    assert names_a != names_b


def test_no_seed_still_reports_a_usable_seed():
    session = engine.create_game()
    assert isinstance(session.seed, int)

    replay = engine.create_game(seed=session.seed)
    names_original = [p.name for p in session.player_generation.list_of_players]
    names_replay = [p.name for p in replay.player_generation.list_of_players]
    assert names_original == names_replay


def test_repeat_sessions_are_isolated():
    random.seed(42)
    session_a = engine.create_game()
    session_b = engine.create_game()

    assert session_a.session_id != session_b.session_id
    assert len({h.display_name for h in session_a.bot_handles}) == engine.NUM_TEAMS
    assert len({h.display_name for h in session_b.bot_handles}) == engine.NUM_TEAMS

    engine.process_bid(session_a, 10)
    assert session_b.current_leader is None
    assert session_b.current_price == engine.STARTING_PRICE


def test_complete_simulation_finishes_the_whole_auction_instantly():
    random.seed(3)
    session = engine.create_game()

    engine.complete_simulation(session)

    assert session.phase == AuctionPhase.GAME_OVER
    assert session.current_player is None

    seen_ids = set()
    total_assigned = 0
    for handle in session.all_handles():
        for player in handle.team.player_list:
            assert player.player_id not in seen_ids
            seen_ids.add(player.player_id)
            total_assigned += 1

    assert total_assigned + len(session.unsold_this_round) == engine.PLAYER_POOL_SIZE


def test_full_game_completes_with_no_duplicate_player_assignment():
    random.seed(7)
    session = engine.create_game()

    steps = 0
    while session.phase != AuctionPhase.GAME_OVER and steps < 10000:
        steps += 1
        if session.phase in (AuctionPhase.SOLD, AuctionPhase.UNSOLD):
            engine.advance(session)
            continue
        if random.random() < 0.3:
            try:
                engine.process_bid(session, random.choice(engine.ALLOWED_INCREMENTS))
                continue
            except InvalidBidError:
                pass
        engine.process_pass(session)

    assert session.phase == AuctionPhase.GAME_OVER

    seen_ids = set()
    total_assigned = 0
    for handle in session.all_handles():
        for player in handle.team.player_list:
            assert player.player_id not in seen_ids
            seen_ids.add(player.player_id)
            total_assigned += 1

    assert total_assigned == len(seen_ids)
    assert total_assigned + len(session.unsold_this_round) == engine.PLAYER_POOL_SIZE
