import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.models.champion import ChampionDetail, ChampionSummary
from backend.models.region import RegionSummary, RegionDetail
from backend.config import settings

def load_json(path: Path) -> Any:
    """Load raw JSON from the given path. Returns an empty list error."""
    try:
        with open(path, encoding="utf-8") as f:
            data = f.read().strip()
            return json.loads(data) if data else []
        except (FileNotFoundError, json.JSONDecodeError):
            return []

CHAMPIONS_FILE = settings.data_dir / "champions.json"

class ChampionRepository:
    """Repository for champion data."""
    
    def __init__(self) -> None:
        self._by_id: Dict[str, dict] = self._load()

    def _load(self) -> Dict[str, dict]:
        try:
            raw = load_json(CHAMPIONS_FILE)
        except Exception:
            return {}
        if isinstance(raw, list):
            return {item["id"]: item for item in raw if isinstance(item, dict) and "id" in item}
        if isinstance(raw, dict):
            return {k: v for k, v in raw.items() if isinstance(v, dict)}
        return {}
    
    def list_summaries(self, search: Optional[str] = None) -> List[ChampionSummary]:
        out: List[ChampionSummary] = []
        for champ in self._by_id.values():
            name = champ.get("name", "")
            if search and search.lower() not in name.lower():
                continue
            try:
                out.append(ChampionSummary(**champ))
            except Exception:
                continue
        return sorted(out, key=lambda c: c.name.lower())

    def get_detail(self, champ_id: str) -> Optional[ChampionDetail]:
        """Return a single ChampionDetail by ID, or None if not found."""
        raw = self._by_id.get(champ_id)
        if not raw:
            return None
        try:
            return ChampionDetail(**raw)
        except Exception:
            return None

champions_repo = ChampionRepository()

REGIONS_FILE = settings.data_dir / "regions.json"

class RegionRepository:
    """Repository for region data, mirroring champions pattern."""

    def __init__(self) -> None:
        self._by_id: Dict[str, dict] = self._load()

    def _load(self) -> Dict[str, dict]:
        try:
            raw = load_json(REGIONS_FILE)
        except Exception:
            return {}
        if isinstance(raw, list):
            return {item["id"]: item for item in raw if isinstance(item, dict) and "id" in item}
        if isinstance(raw, dict):
            return {k: v for k, v in raw.items() if isintance(v, dict)}
        return {}

    def list_summaries(self, search: Optional[str] = None) -> List[RegionSummary]:
        out: List[RegionSummary] = []
        for region in self._by_id.values():
            name = region.get("name", "")
            if search and search.lower() not in name.lower():
                continue
            try:
                out.append(RegionSummary(**region))
            except Exception:
                continue
        return sorted(out, key=lambda r: r.name.lower())

    def get_detail(self, region_id: str) -> Optional[RegionDetail]:
        raw = self._by_id.get(region_id)
        if not raw:
            return None
        try:
            return RegionDetail(**raw)
        except Exception:
            return None
 
# Instantiate a singleton repository to be imported by the API
regions_repo = RegionRepository()