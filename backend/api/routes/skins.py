from typing import List
from fastapi import APIRouter, HTTPException

from backend.models.skin import Skin
from backend.services.loader import skins_repo


router = APIRouter(tags=["skins"])


@router.get("/skins", response_model=list[Skin])
def list_skins():
    """
    Return all skins normalized from ddragon data.
    """
    return skins_repo.list_all()

@router.get("/skins/{skin_id}", response_model=Skin)
def get_skin(skin_id: str):
    """
    Return a single skin by ID.
    """
    skin = skins_repo.get(skin_id)
    if not skin:
        raise HTTPException(status_code=404, detail=f"Skin '{skin_id}' not found")
    return skin