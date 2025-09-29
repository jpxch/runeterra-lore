from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class RegionSummary(BaseModel):
    """Basic region metadata for listings."""
    id: str
    name: str
    icon: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

class RegionDetail(RegionSummary):
    """Full region detail - curated internally, not from ddragon."""
    champions: List[str] = Field(default_factory=list)
    emblem: Optional[str] = None