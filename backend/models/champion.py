from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ChampionSummary(BaseModel):
    """Lightweight model for listing champions."""
    id: str = Field(..., description="Stable champion id/slug (e.g., 'karma').")
    name: str
    region: Optional[str] = None
    icon: Optional[str] = None
    roles: List[str] = []


class ChampionDetail(ChampionSummary):
    """Detailed model for a single champion view."""
    lore: Optional[str] = None
    abilities: Optional[Dict[str, str]] = {}
    skins: List[str] = []