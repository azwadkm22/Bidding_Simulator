from typing import Optional

from pydantic import BaseModel


class BidRequest(BaseModel):
    increment: int


class PlayerCard(BaseModel):
    player_id: int
    name: str
    position: str
    role: str
    nationality: str
    player_type: str
    overall: Optional[int] = None
    batting: int
    bowling: int
    fielding: int
    batting_hand: str
    batting_order: str
    bowling_type: str
    bowling_style: str
    estimated_price: int
    selling_price: Optional[int] = None
    deal_grade: Optional[str] = None
    shortlisted: bool = False


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
    trait: Optional[str] = None
    squad: Optional[list[PlayerCard]] = None
    composition: Optional[TeamComposition] = None
    shortlist: Optional[list[PlayerCard]] = None


class RemainingPlayers(BaseModel):
    count: int
    players: list[PlayerCard]


class StartingElevenResponse(BaseModel):
    key: str
    name: str
    available: bool
    reason: Optional[str] = None
    lineup: list[PlayerCard]
    bench: list[PlayerCard]
    batting_rating: Optional[int] = None
    bowling_rating: Optional[int] = None
    fielding_rating: Optional[int] = None


class NewGameRequest(BaseModel):
    seed: Optional[int] = None
    pool_id: Optional[str] = None


class GeneratePoolRequest(BaseModel):
    seed: Optional[int] = None
    count: Optional[int] = None
    international_count: Optional[int] = None


class PoolSummary(BaseModel):
    pool_id: str
    seed: int
    count: int
    position_counts: dict[str, int]
    bowling_type_counts: dict[str, int]
    player_type_counts: dict[str, int]
    players_above_80: int
    players_above_90: int
    top_batsmen: list[PlayerCard]
    top_bowlers: list[PlayerCard]
    top_allrounders: list[PlayerCard]
    top_wicketkeepers: list[PlayerCard]
    top_openers: list[PlayerCard]
    top_pacers: list[PlayerCard]
    top_spinners: list[PlayerCard]
    most_expensive: list[PlayerCard]


class PoolPlayers(BaseModel):
    count: int
    players: list[PlayerCard]


class SoldPlayerEntry(PlayerCard):
    buyer: str
    buyer_key: str
    is_user: bool


class TeamSummaryEntry(BidderSummary):
    is_user: bool
    starting_eleven: StartingElevenResponse


class GameSummary(BaseModel):
    sold_players: list[SoldPlayerEntry]
    unsold_count: int
    teams: list[TeamSummaryEntry]


class GameState(BaseModel):
    session_id: str
    seed: int
    pool_id: Optional[str] = None
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
