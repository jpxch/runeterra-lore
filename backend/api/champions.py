from fastapi import APIRouter, HTTPException
import json
from pathlib import Path
from models.champion import ChampionSummary, ChampionDetail

router = APIRouter()

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "champions.json"
with open(DATA_PATH, encoding="utf-8") as f:
    _CHAMPIONS = json.load(f)

@router.get("/champions", response_model=list[ChampionSummary])
def list_champions():
    return _CHAMPIONS

@router.get("/champions/{champ_id}", response_model=ChampionDetail)
def get_champion(champ_id: str):
    champ = next((c for c in _CHAMPIONS if c["id"].lower() == champ_id.lower()), None)
    if not champ:
        raise HTTPException(status_code=404, detail="Champion not found")
    return champ