from pydantic import BaseModel
from typing import Optional


class Skin(BaseModel):
    """Standalone skin entry (normalized from champion data)."""
    id: str
    championId: str
    name: str
    num: int
    chromas: bool
    releaseDate: Optional[str] = None
    splash: Optional[str] = None
    loading: Optional[str] = None