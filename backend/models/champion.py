from pydantic import BaseModel
from typing import Dict, List, Optional


class ChampionSummary(BaseModel):
    id: str
    name: str
    region: str
    icon: Optional[str] = None

class ChampionDetail(ChampionSummary):
    lore: str
    abilities: Dict[str, str]
    skins: List[str]