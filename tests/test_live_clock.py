import asyncio

from app.game import engine
from app.services import live_clock
from tests.conftest import make_handle, make_session


def test_auto_tick_progresses_the_auction_without_any_human_action():
    """The clock alone - no process_bid/process_pass call at all - must be
    able to carry a player all the way through bidding to a settled outcome."""

    async def scenario():
        original_tick_seconds = live_clock.TICK_SECONDS
        live_clock.TICK_SECONDS = 0.01
        try:
            bot = make_handle("bot-1", budget=10000, place_bid_result=1)
            session = make_session(bot_handles=[bot])
            initial_log_length = len(session.event_log)

            live_clock.start(session)
            try:
                await asyncio.sleep(0.3)
            finally:
                live_clock.stop(session.session_id)

            return session, initial_log_length
        finally:
            live_clock.TICK_SECONDS = original_tick_seconds

    session, initial_log_length = asyncio.run(scenario())

    # With no queued next player, the lone always-bidding bot should win the
    # player and the session should reach GAME_OVER entirely on its own.
    assert len(session.event_log) > initial_log_length
    assert session.phase == engine.AuctionPhase.GAME_OVER
    assert session.user_handle.team.number_of_players == 0
    assert len(session.bot_handles[0].team.player_list) == 1


def test_paused_session_does_not_advance_on_tick():
    async def scenario():
        original_tick_seconds = live_clock.TICK_SECONDS
        live_clock.TICK_SECONDS = 0.01
        try:
            bot = make_handle("bot-1", budget=10000, place_bid_result=1)
            session = make_session(bot_handles=[bot])
            engine.pause(session)

            live_clock.start(session)
            try:
                await asyncio.sleep(0.1)
            finally:
                live_clock.stop(session.session_id)

            return session
        finally:
            live_clock.TICK_SECONDS = original_tick_seconds

    session = asyncio.run(scenario())

    assert session.phase == engine.AuctionPhase.ON_BLOCK
    assert session.current_leader is None
    assert session.current_price == engine.STARTING_PRICE


def test_resume_lets_the_clock_advance_again():
    async def scenario():
        original_tick_seconds = live_clock.TICK_SECONDS
        live_clock.TICK_SECONDS = 0.01
        try:
            bot = make_handle("bot-1", budget=10000, place_bid_result=1)
            session = make_session(bot_handles=[bot])
            engine.pause(session)

            live_clock.start(session)
            try:
                await asyncio.sleep(0.05)
                assert session.phase == engine.AuctionPhase.ON_BLOCK  # still paused

                engine.resume(session)
                await asyncio.sleep(0.3)
            finally:
                live_clock.stop(session.session_id)

            return session
        finally:
            live_clock.TICK_SECONDS = original_tick_seconds

    session = asyncio.run(scenario())

    # Once resumed, the lone always-bidding bot should carry this (unqueued)
    # session all the way to game over on its own.
    assert session.phase == engine.AuctionPhase.GAME_OVER


def test_stop_cancels_the_background_task():
    async def scenario():
        original_tick_seconds = live_clock.TICK_SECONDS
        live_clock.TICK_SECONDS = 10  # long enough that it won't fire during this test
        try:
            session = make_session()
            live_clock.start(session)
            assert session.session_id in live_clock._tasks
            live_clock.stop(session.session_id)
            await asyncio.sleep(0)  # let the cancellation propagate
            assert session.session_id not in live_clock._tasks
        finally:
            live_clock.TICK_SECONDS = original_tick_seconds

    asyncio.run(scenario())
