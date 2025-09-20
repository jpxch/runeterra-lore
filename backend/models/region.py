from pydantic import BaseModel
from typing import Optional


class Region(BaseModel):
    id: str
    name: str
    description: str
    icon: Optional[str] = None