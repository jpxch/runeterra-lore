from fastapi import APIRouter, HTTPException
from pathlib import Path
import json
from models.region import Region
from services.loader import load_json


router = APIRouter()

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "regions.json"
_REGIONS = load_json(DATA_PATH)

@router.get("/regions", response_model=list[Region])
def list_regions():
    return _REGIONS

@router.get("/regions/{region_id}", response_model=Region)
def get_region(region_id: str):
    region = next((r for r in _REGIONS if r["id"].lower() == region_id.lower()), None)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region