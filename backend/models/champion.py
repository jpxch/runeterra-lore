from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

from .skin import ChampionSkin

class ChampionSummary(BaseModel):
    """Minimal champion metadata used for listing."""
    id: str
    key: str
    name: str
    title: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    icon: Optional[str] = None

    model_config = ConfigDict(extra="ignore")

class ChampionInfo(BaseModel):
    """High-level difficulty/role stats Riot exposes in ddragon."""
    attack: int
    defense: int
    magic: int
    difficulty: int

    model_config = ConfigDict(extra="ignore")

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
    gpregenperlevel: Optional[float] = None

    model_config = ConfigDict(extra="ignore")

class ChampionAbility(BaseModel):
    """Riot-style spell model with the fields you can render in tooltips."""
    id: str
    name: str
    description: str
    icon: str
    cooldown: Optional[List[float]] = None
    cost: Optional[List[int]] = None
    range: Optional[List[int]] = None

    model_config = ConfigDict(extra="ignore")

class ChampionPassive(BaseModel):
    name: str
    description: str
    icon: str

    model_config = ConfigDict(extra="ignore")

class ChampionDetail(ChampionSummary):
    """Full Riot-style champion detail."""
    lore: Optional[str] = None
    info: Optional[ChampionInfo] = None
    stats: Optional[ChampionStats] = None
    passive: Optional[ChampionPassive] = None
    abilities: List[ChampionAbility] = Field(default_factory=list)
    skins: List[ChampionSkin] = Field(default_factory=list)

    model_config = ConfigDict(extra="ignore")