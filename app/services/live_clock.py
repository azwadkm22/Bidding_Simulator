"""Autonomous per-session auction clock (prototype).

The auction no longer waits on a human bid/pass button: each game session
gets a background asyncio task that calls engine.auto_tick on a fixed
interval, so bots keep responding, sold/unsold settles, and the game moves on
to the next player on its own. A human bid/pass/advance submitted through the
normal API at any moment still takes effect immediately; the clock just fills
in whatever the human doesn't act on. engine.pause/resume toggles
session.paused, which this loop checks every tick - the task keeps running
either way, it just skips calling auto_tick while paused.

Correctness here depends on every route in app/api/game.py being declared
`async def` (never plain `def`, which FastAPI would run in a worker thread)
and on every engine function being plain synchronous Python with no internal
`await`. Given both of those, a tick and an incoming request can never
interleave mid-mutation: asyncio's single-threaded event loop always runs one
to completion before the other starts. That's a deliberate simplification for
a single-process, single-worker dev server - it would need real locking (or a
different storage model entirely) before running with multiple workers or
threads.
"""

import asyncio

from app.game import engine

TICK_SECONDS = 1.5

_tasks: dict[str, asyncio.Task] = {}


def start(session: engine.GameSession) -> None:
    task = asyncio.create_task(_run(session))
    _tasks[session.session_id] = task
    task.add_done_callback(lambda _t, sid=session.session_id: _tasks.pop(sid, None))


def stop(session_id: str) -> None:
    task = _tasks.pop(session_id, None)
    if task:
        task.cancel()


async def _run(session: engine.GameSession) -> None:
    while session.phase != engine.AuctionPhase.GAME_OVER:
        await asyncio.sleep(TICK_SECONDS)
        if not session.paused:
            engine.auto_tick(session)
