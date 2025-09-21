from pydantic import BaseModel
from typing import Dict, List, Optional
from models.region import Region
from models.skin import Skin


class ChampionSummary(BaseModel):
    id: str
    name: str
    region: str
    icon: Optional[str] = None

class ChampionDetail(BaseModel):
    id: str
    name: str
    region: Region
    icon: Optional[str] = None
    lore: str
    abilities: Dict[str, str]
    skins: List[Skin]
    relationships: Dict[str, List[str]]