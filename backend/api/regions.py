from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from backend.models.region import RegionSummary, RegionDetail
from backend.services.loader import regions_repo

router = APIRouter(tags=["regions"])

@router.get("/regions", response_model=List[RegionSummary])
def list_regions(search: Optional[str] = Query(default=None, description="Filter by region name")):
    """
    Return all regions, or filter them by case-insensitive substring in the name.
    """
    regions = regions_repo.list_summaries(search)
    return [r.model_dump() for r in regions]


@router.get("/regions/{region_id}", response_model=RegionDetail)
def get_region(region_id: str):
    """
    Return detailed information about a single region.
    """
    region = regions_repo.get_detail(region_id)
    if not region:
        raise HTTPException(status_code=404, detail=f"Region '{region_id}' not found")
    return region.model_dump()