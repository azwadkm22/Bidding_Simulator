"""Data model for the detailed attribute/rating system (player_gen.txt section 2).

Each attribute category is a plain dict rather than a dataclass with
pre-declared fields: "missing is not zero" (section 15) needs a real
distinction between "this key is absent" and "this key is 0", which a dict
gives for free (`.get(path)` returns None only when truly absent).
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DetailedPlayerAttributes:
    player_id: int
    role: str
    primary_bowling_style: str  # "pace" | "spin" | "none"

    batting: dict = field(default_factory=dict)
    paceBowling: dict = field(default_factory=dict)
    spinBowling: dict = field(default_factory=dict)
    fielding: dict = field(default_factory=dict)
    wicketkeeping: dict = field(default_factory=dict)
    physical: dict = field(default_factory=dict)
    mentality: dict = field(default_factory=dict)
    traits: dict = field(default_factory=dict)
    state: dict = field(default_factory=dict)

    # {"pace": {deliveryId: rating, ...}, "spin": {...}} - a style's key absent
    # means "no repertoire data at all" (incomplete); present-but-empty ({})
    # means "no available variations" (valid, quality 0). See section 7.
    repertoire: dict = field(default_factory=dict)

    def get(self, path: str):
        category, _, attribute = path.partition(".")
        bucket = getattr(self, category, None)
        if not isinstance(bucket, dict):
            return None
        return bucket.get(attribute)


@dataclass
class RatingResult:
    raw: float
    displayed: int
    breakdown: Optional[list] = None  # list of (path, value, weight, contribution)


@dataclass
class UnavailableRating:
    missing: list
