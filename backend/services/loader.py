import json
import requests
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.models.champion import ChampionSummary, ChampionDetail, ChampionSkin
from backend.models.skin import Skin
from backend.models.region import RegionSummary, RegionDetail
from backend.config import settings

def load_json(path: Path) -> Any:
    """Load raw JSON from disk, or [] if not found/invalid."""
    try:
        with open(path, encoding="utf-8") as f:
            data = f.read().strip()
            return json.loads(data) if data else []
    except (FileNotFoundError, json.JSONDecodeError):
            return []

def save_json(path: Path, data: Any) -> None:
    """Safely persist data to disk as JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

VERSIONS_URL = "https://ddragon.leagueoflegends.com/api/versions.json"

def get_latest_version() -> str:
    """Fetch the latest patch version from ddragon, or fallback to a safe default."""
    try:
        r = requests.get(VERSIONS_URL, timeout=5)
        r.raise_for_status()
        versions = r.json()
        if isinstance(versions, list) and versions:
            return versions[0]
    except Exception:
        pass
    return "14.18.1"

DDRAGON_VERSION = get_latest_version()
DDRAGON_BASE = f"https://ddragon.leagueoflegends.com/cdn/{DDRAGON_VERSION}/data/en_US"

def fetch_ddragon_data(endpoint: str) -> Optional[dict]:
    """Fetch JSON from ddragon, retun None if request fails."""
    url = f"{DDRAGON_BASE}/{endpoint}"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

CHAMPIONS_FILE = settings.data_dir / "champions.json"

class ChampionRepository:
    """Repository for champion data with ddragon + fallback."""
    
    def __init__(self) -> None:
        self._by_id: Dict[str, dict] = self._load()

    def _load(self) -> Dict[str, dict]:
        raw = fetch_ddragon_data("champion.json")
        if raw and "data" in raw:
            champions = raw["data"]
            save_json(CHAMPIONS_FILE, champions)
            return champions

        cached = load_json(CHAMPIONS_FILE)
        return cached if isinstance(cached, dict) else {}
        
    def list_summaries(self, search: Optional[str] = None) -> List[ChampionSummary]:
        out: List[ChampionSummary] = []
        for champ in self._by_id.values():
            if search and search.lower() not in champ["name"].lower():
                continue
            try:
                out.append(ChampionSummary(
                    id=champ["id"],
                    key=champ["key"],
                    name=champ["name"],
                    title=champ["title"],
                    tags=champ.get("tags", []),
                    icon=f"/cdn/{DDRAGON_VERSION}/img/champion/{champ['image']['full']}"
                ))
            except Exception:
                continue
        return sorted(out, key=lambda c: c.name.lower())

    def get_detail(self, champ_id: str) -> Optional[ChampionDetail]:
        """Return a single ChampionDetail by ID, or None if not found."""
        print(f"DEBUG get_detail called with: {champ_id}")

        champ_key = None
        for cid in self._by_id.keys():
            if cid.lower() == champ_id.lower():
                champ_key = cid
                break
        print(f"DEBUG found champ_key: {champ_key}")

        if not champ_key:
            return None

        detailed_data = fetch_ddragon_data(f"champion/{champ_key}.json")
        if detailed_data and "data" in detailed_data["data"]:
            champ = detailed_data["data"][champ_key]
        else:
            champ = self._by_id[champ_key]
               
        try:
            skins: List[ChampionSkin] = [
                ChampionSkin(
                    id=f"{champ['id'].lower()}_{skin['num']}",
                    num=skin["num"],
                    name=skin["name"],
                    chromas=skin.get("chromas", False),
                    splash=f"/cdn/img/champion/splash/{champ['id']}_{skin['num']}.jpg",
                    loading=f"/cdn/img/champion/loading/{champ['id']}_{skin['num']}.jpg",
                )
                for skin in champ.get("skins", [])
            ]

            return ChampionDetail(
                id=champ["id"],
                key=champ["key"],
                name=champ["name"],
                title=champ.get("title"),
                tags=champ.get("tags", []),
                icon=f"/cdn/{DDRAGON_VERSION}/img/champion/{champ['image']['full']}",
                lore=champ.get("lore") or champ.get("blurb"),
                info=champ.get("info"),
                stats=champ.get("stats"),
                abilities={s["id"]: s["name"] for s in champ.get("spells", [])} if champ.get("spells") else {},
                skins=skins
            )
        except Exception as e:
            print(f"DEBUG failed building {champ['id']}: {e}")
            return None

champions_repo = ChampionRepository()

SKINS_FILE = settings.data_dir / "skins.json"

class SkinRepository:
    """Normnalize skins out of champion repo for standalone / skins API."""
    
    def __init__(self, champions: ChampionRepository) -> None:
        self._all: List[dict] = self._extract(champions._by_id)
        if self._all:
            save_json(SKINS_FILE, self._all)

    def _extract(self, champions: Dict[str, dict]) -> List[dict]:
        out: List[dict] = []
        for champ in champions.values():
            for skin in champ.get("skins", []):
                out.append({
                    "id": f"{champ['id'].lower()}_{skin['num']}",
                    "championId": champ["id"].lower(),
                    "name": skin["name"],
                    "num": skin["num"],
                    "chromas": skin.get("chromas", False),
                    "splash": f"/cdn/img/champion/splash/{champ['id']}_{skin['num']}.jpg",
                    "loading": f"/cdn/img/champion/loading/{champ['id']}_{skin['num']}.jpg",
                })
        return out

    def list_all(self) -> List[Skin]:
        return [Skin(**raw) for raw in self._all]

    def get(self, skin_id: str) -> Optional[Skin]:
        for raw in self._all:
            if raw["id"].lower() == skin_id.lower():
                return Skin(**raw)
        return None

skins_repo = SkinRepository(champions_repo)


REGIONS_FILE = settings.data_dir / "regions.json"

class RegionRepository:
    """Curated region data - not in ddragon."""

    def __init__(self) -> None:
        self._by_id: Dict[str, dict] = self._load()

    def _load(self) -> Dict[str, dict]:
        raw = load_json(REGIONS_FILE)
        if isinstance(raw, list):
            return {item["id"]: item for item in raw if isinstance(item, dict) and "id" in item}
        return {}

    def list_summaries(self, search: Optional[str] = None) -> List[RegionSummary]:
        out: List[RegionSummary] = []
        for region in self._by_id.values():
            if search and search.lower() not in region["name"].lower():
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
 
regions_repo = RegionRepository()