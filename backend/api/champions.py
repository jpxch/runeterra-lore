from fastapi import APIRouter, HTTPException
import json
from pathlib import Path
from models.champion import ChampionSummary, ChampionDetail
from models.region import Region
from models.skin import Skin
from services.loader import load_json

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
_CHAMPIONS = load_json(DATA_DIR / "champions.json")
_REGIONS = {r["id"]: r for r in load_json(DATA_DIR / "regions.json")}
_SKINS = {s["id"]: s for s in load_json(DATA_DIR / "skins.json")}
_RELATIONSHIPS = load_json(DATA_DIR / "relationship.json")

@router.get("/champions", response_model=list[ChampionSummary])
def list_champions():
    return _CHAMPIONS

@router.get("/champions/{champ_id}", response_model=ChampionDetail)
def get_champion(champ_id: str):
    champ = next((c for c in _CHAMPIONS if c["id"].lower() == champ_id.lower()), None)
    if not champ:
        raise HTTPException(status_code=404, detail="Champion not found")
    
    skins = [ _SKINS[skin_id] for skin_id in champ.get("skinIds", []) if skin_id in _SKINS ]
    relationships = rel.get("relationships") if rel else {"allies": [], "rivals": []}

    return {
        "id": champ["id"],
        "name": champ["name"],
        "region": region,
        "icon": champ.get("icon"),
        "lore": champ["lore"],
        "abilities": champ["abilities"],
        "skins": skins,
        "relationships": relationships,
    }