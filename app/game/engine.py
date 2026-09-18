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

from app.game.player_pool import DEFAULT_POOL_SIZE, PlayerPool, instantiate_players

NUM_TEAMS = 12
PLAYER_POOL_SIZE = DEFAULT_POOL_SIZE
STARTING_PRICE = 10
USER_TEAM_ID = -1
USER_TEAM_NAME = "Your Team"
USER_STARTING_BUDGET = 2000
MAX_SQUAD_SIZE = 21
ALLOWED_INCREMENTS = [5, 10, 25, 50]
SILENT_ROUNDS_TO_UNSOLD = 3
SILENT_ROUNDS_TO_SOLD = 2

# Bot bid increments scale with how far price sits relative to the player's
# estimated value (below ratio threshold, increment choices) - not a hump,
# a "ramp then cool off": tentative while still a bargain, biggest jumps while
# a real bidding war pushes price up toward and just past fair value, then
# smaller cautious steps once the price is already well above what the player
# is worth. Mirrors how real bidders get bolder approaching value and more
# hesitant once they're clearly overpaying, instead of a flat step size or one
# that keeps growing no matter how inflated the price already is.
BOT_INCREMENT_TIERS = [
    (0.5, [3, 5, 8]),
    (1.0, [8, 15, 25]),
    (1.5, [15, 25, 40]),
    (float("inf"), [5, 10, 15]),
]


def _bot_increment_choices(current_price: int, estimated_price: int) -> list:
    ratio = current_price / max(estimated_price, 1)
    for threshold, choices in BOT_INCREMENT_TIERS:
        if ratio < threshold:
            return choices
    return BOT_INCREMENT_TIERS[-1][1]


# Deal-grade thresholds: `bargain` is (estimated - paid) / estimated, so
# positive means a discount and negative means an overpay. `fit` is how badly
# the buying team needed this player (Team.find_new_player_priority,
# normalized), evaluated before the player joins the squad. A grade can only
# reach A when the price was a genuine bargain AND it filled a real gap -
# either alone caps out at B, matching "cheap but also adds value to the
# squad" rather than treating either factor as sufficient on its own.
DEAL_GRADE_BARGAIN_GREAT = 0.25
DEAL_GRADE_BARGAIN_FAIR = -0.05
DEAL_GRADE_BARGAIN_POOR = -0.30
DEAL_GRADE_FIT_THRESHOLD = 0.35
DEAL_GRADE_FIT_MAX_PRIORITY = 8.0


def _grade_deal(handle: "BidderHandle", player: Player, price: int) -> str:
    estimated = max(player.estimated_price, 1)
    bargain = (estimated - price) / estimated
    priority = handle.team.find_new_player_priority(player)
    fit = max(0.0, min(1.0, priority / DEAL_GRADE_FIT_MAX_PRIORITY))
    needed = fit >= DEAL_GRADE_FIT_THRESHOLD

    if bargain >= DEAL_GRADE_BARGAIN_GREAT:
        return "A" if needed else "B"
    if bargain >= DEAL_GRADE_BARGAIN_FAIR:
        return "B" if needed else "C"
    if bargain >= DEAL_GRADE_BARGAIN_POOR:
        return "C"
    return "D"


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
    seed: int = 0
    # The PlayerPool this session was started from, if any (see
    # app/game/player_pool.py) - lets the frontend fetch a player's detailed
    # attributes (Player/ratings/) mid-auction via the same
    # /api/players/{pool_id}/players/{player_id}/detail endpoint the
    # generation screen uses. None for the legacy ad-hoc seed-only path.
    pool_id: Optional[str] = None

    def all_handles(self):
        return [self.user_handle] + self.bot_handles

    def find_handle(self, key: str) -> Optional[BidderHandle]:
        for handle in self.all_handles():
            if handle.key == key:
                return handle
        return None


def _log(session: GameSession, message: str) -> None:
    session.event_log.append(message)


SEED_MAX = 2**31 - 1


def create_game(seed: Optional[int] = None, player_pool: Optional[PlayerPool] = None) -> GameSession:
    """Starts a new auction session.

    If `player_pool` is given (see app/game/player_pool.py), the auction uses
    that pool's players - generated as a separate, reviewable step - via
    fresh Player objects reconstructed from its snapshot, so reusing the same
    pool for a second auction never carries over selling_price/deal_grade
    from the first one. `seed` is ignored in that case; session.seed just
    records the pool's own seed for display.

    Otherwise this falls back to the original ad-hoc path: reseed the
    process-wide random module and generate a fresh pool inline. Same caveat
    either way - reseeding is global, since no domain code (Player/Team
    generation, bidder decisions) accepts an injectable RNG. That means
    generating/starting something seeded while another session's live clock
    is still ticking in the background will perturb that other session's
    randomness too. Fine for the one-game-at-a-time way this app is meant to
    be used; would need every domain call site threaded with its own
    random.Random instance to be safe with multiple concurrent sessions.
    """
    if player_pool is not None:
        players = instantiate_players(player_pool)
        seed = player_pool.seed
    else:
        if seed is None:
            seed = random.randint(0, SEED_MAX)
        random.seed(seed)
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
        seed=seed,
        pool_id=player_pool.pool_id if player_pool is not None else None,
    )
    _log(session, f"Auction started (seed {seed}): {len(players)} players, 12 rival teams. Good luck!")
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


def _core_skill(player: Player) -> float:
    if player.position == "Bowler":
        return player.bowling
    if player.position == "Allrounder":
        return (player.batting + player.bowling) / 2
    return player.batting  # Batsmen, Wicketkeeper, Trainee


def _skill_factor(player: Player) -> float:
    # 0.1 floor at/below skill 40, ramps to 1.0 (no damping) at skill 80+.
    return max(0.1, min(1.0, (_core_skill(player) - 40) / 40))


def _bot_wants_to_bid(handle: BidderHandle, player: Player, candidate_price: int) -> bool:
    """Whether a bot accepts a candidate price, using the domain bidder's own
    calculate_utility score but damping it for players whose own skill is
    weak.

    UtilityBasedBidder.calculate_utility mixes a player's own quality with
    "does this team need bodies right now" (open roster slots, affordable
    price relative to remaining budget) - both of which give every bot the
    same flat bonus no matter how weak the specific player is. Early in an
    auction, when every team has open slots, that desperation signal can
    swamp the actual skill signal, so mediocre players get bid up almost as
    hard as stars purely because slots are open. This doesn't touch
    calculate_utility itself (a large, delicately-tuned function); it only
    scales its positive output down for weak players before the accept/reject
    roll, leaving placeBid's own probabilistic decision path for anything
    that isn't a UtilityBasedBidder.
    """
    bidder = handle.bidder
    if not hasattr(bidder, "calculate_utility"):
        return bidder.placeBid(player, candidate_price) == 1

    if handle.team.number_of_players > MAX_SQUAD_SIZE - 1:
        return False

    utility = bidder.calculate_utility(player, candidate_price)
    if utility > 0:
        utility *= _skill_factor(player)

    if utility < 0:
        return False
    if utility > 1:
        return True
    return random.random() < utility


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
    increment_choices = _bot_increment_choices(base_price, session.current_player.estimated_price)
    contenders = []
    for handle in session.bot_handles:
        if session.current_leader is handle:
            continue
        candidate_increment = random.choice(increment_choices)
        candidate_price = base_price + candidate_increment
        if _bot_wants_to_bid(handle, session.current_player, candidate_price):
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

    # Grade before adding to the team, since it needs to be based on how much
    # this fills a gap in the *pre-purchase* squad, not the post-purchase one.
    grade = _grade_deal(leader, player, price)

    leader.bidder.subtractPrice(price)
    player.setSellingPrice(price)
    player.deal_grade = grade
    leader.bidder.addPlayerToTeam(player)

    session.phase = AuctionPhase.SOLD
    session.last_result = {
        "type": "sold",
        "player_id": player.player_id,
        "player_name": player.name,
        "price": price,
        "winner": leader.display_name,
        "is_user": leader.is_user,
        "deal_grade": grade,
    }
    _log(session, f"SOLD! {player.name} goes to {leader.display_name} for {price} (Grade {grade}).")


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
