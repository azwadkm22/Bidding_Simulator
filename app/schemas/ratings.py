from typing import Optional

from pydantic import BaseModel


class AttributeBreakdownEntry(BaseModel):
    path: str
    value: float
    weight: float
    contribution: float


class RatingValue(BaseModel):
    raw: Optional[float] = None
    displayed: Optional[int] = None
    unavailable: bool = False
    missing: Optional[list[str]] = None
    breakdown: Optional[list[AttributeBreakdownEntry]] = None


class PlayerDetailResponse(BaseModel):
    player_id: int
    name: str
    position: str
    role: str
    primary_bowling_style: str
    batting_hand: str
    batting_order: str
    nationality: str
    player_type: str
    core: dict[str, float]
    ratings: dict[str, RatingValue]
    attributes: dict


class WeightTablesResponse(BaseModel):
    """Every weight table plus the batting vs-matchup blend, straight from
    Player/ratings/weights.py, so the Create Player tool can build its form
    and show live weight percentages without hardcoding attribute lists.
    """

    tables: dict[str, list[tuple[str, float]]]
    role_overall: dict[str, dict[str, float]]
    batting_vs_blend: dict[str, float]


class CustomPlayerAttributes(BaseModel):
    batting: dict[str, float] = {}
    paceBowling: dict[str, float] = {}
    spinBowling: dict[str, float] = {}
    fielding: dict[str, float] = {}
    wicketkeeping: dict[str, float] = {}
    physical: dict[str, float] = {}
    mentality: dict[str, float] = {}


class CustomPlayerPreviewRequest(BaseModel):
    role: str
    primary_bowling_style: str = "none"
    attributes: CustomPlayerAttributes


class CustomPlayerCreateRequest(CustomPlayerPreviewRequest):
    name: str = "Custom Player"
    position: str
    batting_hand: str = "Right"
    bowling_type: str = "Pacer"
    batting_order: str = "Middle Order"
    fame: int = 50
    player_type: str = "Domestic"
