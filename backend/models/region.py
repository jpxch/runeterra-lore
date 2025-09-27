from typing import List, Optional
from pydantic import BaseModel

class RegionSummary(BaseModel):
    """Basic region metadata for listings."""
    id: str
    name: str
    icon: Optional[str] = None

class RegionDetail(RegionSummary):
    """Full region detail - curated interanlly, not from ddragon."""
    description: Optional[str] = None
    champions: List[str] = []
    emblem: Optional[str] = None