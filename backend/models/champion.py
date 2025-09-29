from typing import Dict, List, Optional
from pydantic import BaseModel


class ChampionInfo(BaseModel):
    """High-level difficulty/role stats Riot exposes in ddragon."""
    attack: int
    defense: int
    magic: int
    difficulty: int

class ChampionStats(BaseModel):
    """Detailed numeric stats per champion."""
    hp: float
    hpperlevel: float
    mp: float
    mpperlevel: Optional[float] = None
    movespeed: float
    armor: float
    armorperlevel: float
    spellblock: float
    spellblockperlevel: float
    attackrange: float
    hpregen: float
    hpregenperlevel: Optional[float] = None
    mpregen: float
    mpregenperlevel: float
    crit: float
    critperlevel: float
    attackdamage: float
    attackdamageperlevel: float
    attackspeedperlevel: float
    attackspeed: float

class ChampionSkin(BaseModel):
    """Skin metadata (embedded inside ChampionDetail)."""
    id: str
    num: int
    name: str
    chromas: bool
    splash: Optional[str] = None
    loading: Optional[str] = None

class ChampionSummary(BaseModel):
    """Lightweight list view for champions."""
    id: str
    key: str
    name: str
    title: str
    tags: List[str]
    icon: Optional[str] = None

class ChampionDetail(ChampionSummary):
    """Full Riot-style champion detail."""
    lore: Optional[str] = None
    info: Optional[ChampionInfo] = None
    stats: Optional[ChampionStats] = None
    skins: List[ChampionSkin] = []
    abilities: Dict[str, str] = {}