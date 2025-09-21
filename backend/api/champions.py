from fastapi import APIRouter, HTTPException
from typing import List

from backend.services.loader import load_json
from backend.models.champion import ChampionSummary, ChampionDetail

router = APIRouter()


@router.get("/champions", response_model=List[ChampionSummary])
def get_champions():
    """
    Return a list of champions with summary fields.
    """
    data = load_json("data/champions.json")
    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail="Invalid champions data")
    
    return [
        ChampionSummary(**champ) for champ in data
    ]


@router.get("/champions/{champion_id}", response_model=ChampionDetail)
def get_champion(champion_id: str):
    """
    Return detailed information about a single champion.
    """
    data = load_json("data/champions.json")
    if not isinstance(data, list):
        raise HTTPException(status_code=500, detail="Invalid champions data")

    for champ in data:
        if champ.get("id") == champion_id:
            return ChampionDetail(**champ)

    raise HTTPException(status_code=404, detail="Champion not found")
