from fastapi import APIRouter, HTTPException
import json
from pathlib import Path

router = APIRouter()

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "champions.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    _CHAMPIONS = json.load(f)

def _summary(ch):
    return {
        "id": ch["id"],
        "name": ch["name"],
        "region": ch["region"],
        "icon": ch.get["icon"]
    }

@router.get("/champions")
def list_champions():
    return [_summary(c) for c in _CHAMPIONS]

@router.get("/champions/{champ_id}")
def get_champion(champ_id: str):
    champ_id = champ_id.lower()
    for c in _CHAMPIONS:
        if c["id"].lower() == champ_id:
            return c
    raise HTTPException(status_code=404, detail="Champion not found")