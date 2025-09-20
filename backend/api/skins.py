from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from models.skin import Skin
from services.loader import load_json


router = APIRouter()

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "skins.json"
_SKINS = load_json(DATA_PATH)


@router.get("/skins", response_model=list[Skin])
def list_skins():
    return _SKINS

@router.get("/skins/{skin_id}", response_model=Skin)
def get_skin(skin_id: str):
    skin = next((s for s in _SKINS if s["id"].lower() == skin_id.lower()), None)
    if not skin:
        raise HTTPException(status_code=404, detail="Skin not found")
    return skin