from pydantic import BaseModel
from typing import Optional


class Skin(BaseModel):
    """Standalone skin entry (normalized from champion data)."""
    id: str
    champion_id: str
    name: str
    num: int
    chromas: bool
    release_date: Optional[str] = None
    splash: Optional[str] = None
    loading: Optional[str] = None

class ChampionSkinSummary(BaseModel):
    """Lightweight reference used inside ChampionDetail."""
    id: str
    num: int
    name: str
    chromas: bool
    splash: Optional[str] = None
    loading: Optional[str] = None