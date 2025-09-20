from pydantic import BaseModel
from typing import Optional
from datetime import date


class Skin(BaseModel):
    id: str
    championId: str
    name: str
    releaseDate: Optional[date] = None
    splash: Optional[str] = None