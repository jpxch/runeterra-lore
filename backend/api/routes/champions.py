from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from backend.models.champion import ChampionDetail, ChampionSummary
from backend.services.loader import champions_repo

router = APIRouter(tags=["champions"])


@router.get("/champions", response_model=List[ChampionSummary])
def list_champions(
    search: Optional[str] = Query(default=None, description="Filter champions by namesubstring"),
) -> List[ChampionSummary]:
    """
    Return all champions, or filter them by a case-insensitive substring in the name.
    """
    return champions_repo.list_summaries(search)


@router.get("/champions/{champion_id}", response_model=ChampionDetail)
def get_champion(champion_id: str) -> ChampionDetail:
    """
    Return detailed information about a single champion.
    """
    champion = champions_repo.get_detail(champion_id)
    if champion is None:
        raise HTTPException(status_code=404, detail=f"Champion '{champion_id}' not found")
    return champion
