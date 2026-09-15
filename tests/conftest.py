from collections import deque

from Player.player import Player
from Team.team import Team

from app.game.engine import AuctionPhase, BidderHandle, GameSession


class DummyTeamGeneration:
    """Stand-in for TeamGenStat: engine only ever reads .rivals_for_players."""

    def __init__(self):
        self.rivals_for_players = {}


class FakeBidder:
    """Minimal stand-in for UserBidder/UtilityBasedBidder.

    The engine only ever calls .placeBid / .subtractPrice / .addPlayerToTeam
    and reads .budget, so this is enough to drive engine tests deterministically
    without depending on the real (randomized) bidding strategies.
    """

    def __init__(self, budget, place_bid_result=0):
        self.budget = budget
        self.team = None
        self._place_bid_result = place_bid_result

    def placeBid(self, player, price):
        if callable(self._place_bid_result):
            return self._place_bid_result(player, price)
        return self._place_bid_result

    def subtractPrice(self, price):
        self.budget -= price

    def addPlayerToTeam(self, player):
        self.team.addPlayer(player)


def make_player(player_id=1, name="Test Player", estimated_price=50, position="Batsmen"):
    return Player(
        player_id=player_id,
        json_data={
            "name": name,
            "batting": 75,
            "bowling": 20,
            "fielding": 60,
            "position": position,
            "fame": 50,
            "estimated_price": estimated_price,
            "batting_hand": "Right",
            "bowling_type": "Pacer",
            "bowling_style": "Medium",
            "batting_order": "Top Order",
            "selling_price": 0,
        },
    )


def make_handle(key, budget=1000, place_bid_result=0, is_user=False, team_id=1):
    team = Team(team_id, key)
    bidder = FakeBidder(budget, place_bid_result)
    bidder.team = team
    return BidderHandle(key=key, display_name=key, team=team, bidder=bidder, is_user=is_user)


def make_session(player=None, user_budget=1000, user_place_bid_result=0, bot_handles=None):
    player = player or make_player()
    user_handle = make_handle("user", budget=user_budget, place_bid_result=user_place_bid_result, is_user=True, team_id=-1)
    session = GameSession(
        session_id="test-session",
        player_generation=None,
        team_generation=DummyTeamGeneration(),
        user_handle=user_handle,
        bot_handles=bot_handles or [],
        queue=deque(),
    )
    session.current_player = player
    session.current_price = 10
    session.current_leader = None
    session.phase = AuctionPhase.ON_BLOCK
    return session
