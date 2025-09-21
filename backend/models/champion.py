from typing import List, Optional
from pydantic import BaseModel


class ChampionSummary(BaseModel):
    """Lightweight model for listing champions."""
    id: str
    name: str
    region: Optional[str] = None
    roles: List[str]


class ChampionDetail(ChampionSummary):
    """Detailed model for a single champion view."""
    lore: Optional[str] = None
    abilities: Optional[List[str]] = []
    skins: Optional[List[str]] = []