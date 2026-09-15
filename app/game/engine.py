"""State-driven auction engine.

Replaces the blocking input()/print()/time.sleep() loop in bidding_simulation.py
with explicit state transitions driven by discrete calls (process_bid,
process_pass, advance). Domain classes (Player, Team, UtilityBasedBidder,
UserBidder) are reused unchanged; this module only orchestrates them.

One shared `_apply_bid` gate is used for both the human and every bot bid, so
budget/squad-size checks and the price an AI evaluates vs. the price it pays
are guaranteed consistent between the two paths.
"""

import random
import uuid
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from Bidders.user_bidder import UserBidder
from Bidders.utility_based_bidder import UtilityBasedBidder
from Player.generate_players import get_list_of_players
from Player.player import Player
from Player.player_generation_stats import PlayerGenStat
from Team.generate_teams import generate_teams, generate_bidders
from Team.team import Team
from Team.team_generation_stats import TeamGenStat

NUM_TEAMS = 12
PLAYER_POOL_SIZE = 250
STARTING_PRICE = 10
USER_TEAM_ID = -1
USER_TEAM_NAME = "Your Team"
USER_STARTING_BUDGET = 20000
MAX_SQUAD_SIZE = 21
ALLOWED_INCREMENTS = [5, 10, 25, 50]
SILENT_ROUNDS_TO_UNSOLD = 3
SILENT_ROUNDS_TO_SOLD = 2

# Bot bid increments scale with the current price itself (below threshold,
# increment choices): early jockeying over any player starts small, but once
# a real bidding war pushes the price up, jumps get bigger fast instead of
# crawling up by the same tiny step every round regardless of how contested
# the player is.
BOT_INCREMENT_TIERS = [
    (30, [3, 5, 8]),
    (80, [8, 12, 18]),
    (150, [15, 25, 35]),
    (float("inf"), [30, 50, 75]),
]


def _bot_increment_choices(current_price: int) -> list:
    for threshold, choices in BOT_INCREMENT_TIERS:
        if current_price < threshold:
            return choices
    return BOT_INCREMENT_TIERS[-1][1]


class AuctionPhase(str, Enum):
    ON_BLOCK = "on_block"
    GOING_ONCE = "going_once"
    GOING_TWICE = "going_twice"
    SOLD = "sold"
    UNSOLD = "unsold"
    GAME_OVER = "game_over"


OPEN_PHASES = (AuctionPhase.ON_BLOCK, AuctionPhase.GOING_ONCE, AuctionPhase.GOING_TWICE)
DECIDED_PHASES = (AuctionPhase.SOLD, AuctionPhase.UNSOLD)


class InvalidBidError(Exception):
    pass


@dataclass
class BidderHandle:
    key: str
    display_name: str
    team: Team
    bidder: object
    is_user: bool


@dataclass
class GameSession:
    session_id: str
    player_generation: PlayerGenStat
    team_generation: TeamGenStat
    user_handle: BidderHandle
    bot_handles: list
    queue: deque = field(default_factory=deque)
    unsold_this_round: list = field(default_factory=list)
    round_number: int = 1
    current_player: Optional[Player] = None
    current_price: int = 0
    current_leader: Optional[BidderHandle] = None
    phase: AuctionPhase = AuctionPhase.ON_BLOCK
    silent_rounds: int = 0
    hold_rounds: int = 0
    event_log: list = field(default_factory=list)
    last_result: Optional[dict] = None
    paused: bool = False

    def all_handles(self):
        return [self.user_handle] + self.bot_handles

    def find_handle(self, key: str) -> Optional[BidderHandle]:
        for handle in self.all_handles():
            if handle.key == key:
                return handle
        return None


def _log(session: GameSession, message: str) -> None:
    session.event_log.append(message)


def create_game() -> GameSession:
    players = get_list_of_players(PLAYER_POOL_SIZE)
    players = sorted(players, key=lambda p: p.estimated_price, reverse=True)
    player_generation = PlayerGenStat(players)

    team_list = generate_teams(NUM_TEAMS)
    team_generation = TeamGenStat(team_list=team_list, player_generation=player_generation)
    bot_bidders = generate_bidders(NUM_TEAMS, team_generation)

    bot_handles = [
        BidderHandle(
            key=f"bot-{team.team_id}",
            display_name=team.name,
            team=team,
            bidder=bidder,
            is_user=False,
        )
        for team, bidder in zip(team_list, bot_bidders)
    ]

    user_team = Team(USER_TEAM_ID, USER_TEAM_NAME)
    user_bidder = UserBidder(USER_TEAM_NAME, USER_STARTING_BUDGET, user_team)
    user_handle = BidderHandle(
        key="user",
        display_name=USER_TEAM_NAME,
        team=user_team,
        bidder=user_bidder,
        is_user=True,
    )

    session = GameSession(
        session_id=str(uuid.uuid4()),
        player_generation=player_generation,
        team_generation=team_generation,
        user_handle=user_handle,
        bot_handles=bot_handles,
        queue=deque(player_generation.list_of_players),
    )
    _log(session, "Auction started: 250 players, 12 rival teams. Good luck!")
    _load_next_player(session)
    return session


def _require_open_phase(session: GameSession) -> None:
    if session.phase == AuctionPhase.GAME_OVER:
        raise InvalidBidError("Auction is already complete.")
    if session.phase in DECIDED_PHASES:
        raise InvalidBidError("This player's outcome is decided; call advance to continue.")
    if session.current_player is None:
        raise InvalidBidError("Auction is not currently active.")


def _apply_bid(session: GameSession, handle: BidderHandle, amount: int) -> int:
    if amount <= 0:
        raise InvalidBidError("Bid increment must be a positive number.")
    if session.current_leader is handle:
        raise InvalidBidError("You are already the leading bidder.")
    if handle.team.number_of_players > MAX_SQUAD_SIZE - 1:
        raise InvalidBidError("Squad is full.")
    new_price = session.current_price + amount
    if new_price > handle.bidder.budget:
        raise InvalidBidError("Bid exceeds available budget.")
    session.current_price = new_price
    session.current_leader = handle
    return new_price


def process_bid(session: GameSession, amount: int) -> GameSession:
    _require_open_phase(session)
    _apply_bid(session, session.user_handle, amount)
    _log(session, f"You bid. {session.current_player.name}'s price is now {session.current_price}.")
    _run_bot_sweep(session)
    _evaluate_phase(session, bid_happened_this_round=True)
    return session


def process_pass(session: GameSession) -> GameSession:
    _require_open_phase(session)
    _log(session, "You pass.")
    bid_happened = _run_bot_sweep(session)
    _evaluate_phase(session, bid_happened_this_round=bid_happened)
    return session


MAX_SKIP_ROUNDS = 500


def skip_to_outcome(session: GameSession) -> GameSession:
    """Resolve the current player's bidding instantly instead of waiting on
    the live clock's real-time pacing: repeats the same silent-round step the
    clock would (bots respond, phase evaluated) as fast as Python can, with no
    sleep between rounds, until the outcome is decided. Stops at sold/unsold -
    it does not also skip past the reveal; the live clock or a manual advance
    still moves on to the next player.
    """
    _require_open_phase(session)
    rounds = 0
    while session.phase in OPEN_PHASES and rounds < MAX_SKIP_ROUNDS:
        bid_happened = _run_bot_sweep(session)
        _evaluate_phase(session, bid_happened_this_round=bid_happened)
        rounds += 1
    return session


def auto_tick(session: GameSession) -> GameSession:
    """What happens on a clock tick when the human hasn't acted this round.

    Lets the auction run on its own pace instead of blocking on a bid/pass
    button: bots still get to respond, sold/unsold settlement still happens,
    and the auction still moves on to the next player - all without any
    human action. A human bid/pass submitted at any moment still takes effect
    immediately through process_bid/process_pass; this is only what fills the
    silence between those.
    """
    if session.phase in DECIDED_PHASES:
        advance(session)
    elif session.phase in OPEN_PHASES:
        bid_happened = _run_bot_sweep(session)
        _evaluate_phase(session, bid_happened_this_round=bid_happened)
    return session


MAX_SIMULATION_STEPS = 100_000


def complete_simulation(session: GameSession) -> GameSession:
    """Fast-forward the entire rest of the auction instantly - every
    remaining player, not just the one on the block. Same building blocks as
    auto_tick/skip_to_outcome, just repeated with no pacing and no human
    involvement until the game is over.
    """
    steps = 0
    while session.phase != AuctionPhase.GAME_OVER and steps < MAX_SIMULATION_STEPS:
        auto_tick(session)
        steps += 1
    return session


def pause(session: GameSession) -> GameSession:
    """Stop the autonomous live clock from advancing this session.

    Manual actions (process_bid/process_pass/skip_to_outcome/advance) are
    unaffected and still work while paused - this only stops the background
    clock (see services/live_clock.py) from acting on the human's behalf.
    """
    if not session.paused:
        session.paused = True
        _log(session, "Auction paused.")
    return session


def resume(session: GameSession) -> GameSession:
    if session.paused:
        session.paused = False
        _log(session, "Auction resumed.")
    return session


def _run_bot_sweep(session: GameSession) -> bool:
    """One round of bot bidding, modeled as simultaneous rather than sequential.

    Every eligible bot evaluates the same starting price independently (none
    of them sees another's decision this round), rather than seeing prices
    already bumped by bots evaluated earlier in the same pass. Among every bot
    willing to bid, the highest offer wins the round and is the only one
    applied - a single round can still only move the price once, which keeps
    settlement atomic and the human/bot validation path shared via
    _apply_bid.
    """
    base_price = session.current_price
    increment_choices = _bot_increment_choices(base_price)
    contenders = []
    for handle in session.bot_handles:
        if session.current_leader is handle:
            continue
        candidate_increment = random.choice(increment_choices)
        candidate_price = base_price + candidate_increment
        if handle.bidder.placeBid(session.current_player, candidate_price) == 1:
            contenders.append((handle, candidate_increment, candidate_price))

    if not contenders:
        return False

    random.shuffle(contenders)  # randomize the order equal-price ties are tried in
    contenders.sort(key=lambda c: c[2], reverse=True)

    for handle, increment, _price in contenders:
        try:
            _apply_bid(session, handle, increment)
        except InvalidBidError:
            continue
        others = len(contenders) - 1
        interest_note = f" ({others} other team{'s' if others != 1 else ''} also showed interest.)" if others else ""
        _log(session, f"{handle.display_name} takes it at {session.current_price}.{interest_note}")
        return True

    return False


def _evaluate_phase(session: GameSession, bid_happened_this_round: bool) -> None:
    if bid_happened_this_round:
        session.hold_rounds = 0
        session.silent_rounds = 0
        session.phase = AuctionPhase.GOING_ONCE
        return

    if session.current_leader is None:
        session.silent_rounds += 1
        if session.silent_rounds >= SILENT_ROUNDS_TO_UNSOLD:
            _mark_unsold(session)
        else:
            session.phase = AuctionPhase.ON_BLOCK
    else:
        session.hold_rounds += 1
        if session.hold_rounds >= SILENT_ROUNDS_TO_SOLD:
            _settle_sale(session)
        else:
            session.phase = AuctionPhase.GOING_TWICE


def _settle_sale(session: GameSession) -> None:
    player = session.current_player
    leader = session.current_leader
    price = session.current_price

    leader.bidder.subtractPrice(price)
    player.setSellingPrice(price)
    leader.bidder.addPlayerToTeam(player)

    session.phase = AuctionPhase.SOLD
    session.last_result = {
        "type": "sold",
        "player_id": player.player_id,
        "player_name": player.name,
        "price": price,
        "winner": leader.display_name,
        "is_user": leader.is_user,
    }
    _log(session, f"SOLD! {player.name} goes to {leader.display_name} for {price}.")


def _mark_unsold(session: GameSession) -> None:
    player = session.current_player
    session.unsold_this_round.append(player)
    session.phase = AuctionPhase.UNSOLD
    session.last_result = {
        "type": "unsold",
        "player_id": player.player_id,
        "player_name": player.name,
    }
    _log(session, f"{player.name} went unsold.")


def advance(session: GameSession) -> GameSession:
    if session.phase == AuctionPhase.GAME_OVER:
        raise InvalidBidError("Auction is already complete.")
    if session.phase not in (AuctionPhase.SOLD, AuctionPhase.UNSOLD):
        raise InvalidBidError("This player's auction is still open; bid or pass instead.")
    session.last_result = None
    _load_next_player(session)
    return session


def _load_next_player(session: GameSession) -> None:
    if not session.queue:
        if session.round_number == 1 and session.unsold_this_round:
            session.round_number = 2
            session.queue = deque(session.unsold_this_round)
            session.unsold_this_round = []
            _log(session, "Round 2 begins: revisiting players who went unsold.")
        else:
            session.current_player = None
            session.phase = AuctionPhase.GAME_OVER
            _log(session, "Auction complete.")
            return

    session.current_player = session.queue.popleft()
    session.current_price = STARTING_PRICE
    session.current_leader = None
    session.silent_rounds = 0
    session.hold_rounds = 0
    session.phase = AuctionPhase.ON_BLOCK

    rivals = session.team_generation.rivals_for_players.get(session.current_player)
    if rivals:
        _log(session, f"{session.current_player.name} steps up. Teams eyeing him: {', '.join(rivals)}.")
    else:
        _log(session, f"{session.current_player.name} steps up for auction.")
