from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()

@router.get("/champions")
def get_champions():
    path = Path(__file__).parent.parent.parent / "data" / "champions.json"
    with open(path) as f:
        champions = json.load(f)
    return champions