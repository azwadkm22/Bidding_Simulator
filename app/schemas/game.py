from typing import Optional

from pydantic import BaseModel


class BidRequest(BaseModel):
    increment: int


class PlayerCard(BaseModel):
    player_id: int
    name: str
    position: str
    batting: int
    bowling: int
    fielding: int
    batting_hand: str
    batting_order: str
    bowling_type: str
    bowling_style: str
    estimated_price: int
    selling_price: Optional[int] = None


class TeamComposition(BaseModel):
    batsmen: int
    bowlers: int
    allrounders: int
    wicketkeepers: int


class BidderSummary(BaseModel):
    key: str
    name: str
    budget: float
    squad_size: int
    squad: Optional[list[PlayerCard]] = None
    composition: Optional[TeamComposition] = None


class RemainingPlayers(BaseModel):
    count: int
    players: list[PlayerCard]


class GameState(BaseModel):
    session_id: str
    phase: str
    paused: bool
    round_number: int
    players_remaining: int
    current_player: Optional[PlayerCard] = None
    current_price: int
    current_leader: Optional[str] = None
    available_actions: list[str]
    last_result: Optional[dict] = None
    allowed_increments: list[int]
    user: BidderSummary
    rivals: list[BidderSummary]
    event_log: list[str]
