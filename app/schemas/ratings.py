from typing import Optional

from pydantic import BaseModel


class RatingValue(BaseModel):
    raw: Optional[float] = None
    displayed: Optional[int] = None
    unavailable: bool = False
    missing: Optional[list[str]] = None


class PlayerDetailResponse(BaseModel):
    player_id: int
    name: str
    position: str
    role: str
    primary_bowling_style: str
    core: dict[str, float]
    ratings: dict[str, RatingValue]
    attributes: dict
