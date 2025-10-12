import json
import requests
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.models.champion import (
    ChampionDetail,
    ChampionInfo,
    ChampionStats,
    ChampionAbility,
    ChampionPassive,
)
from backend.models.skin import ChampionSkin
from backend.models.region import RegionSummary, RegionDetail
from backend.core.config import settings

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
    """Fetch JSON from ddragon, return None if request fails."""
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
        champ_key = next((cid for cid in self._by_id.keys() if cid.lower() == champ_id.lower()), None)
        if not champ_key:
            return None

        detailed = fetch_ddragon_data(f"champion/{champ_key}.json")
        if not detailed or "data" not in detailed or champ_key not in detailed["data"]:
            return None

        champ = detailed["data"][champ_key]

        abilities: List[ChampionAbility] = []
        for spell in champ.get("spells", []) or []:
            try:
                abilities.append(
                    ChampionAbility(
                        id=spell["id"],
                        name=spell["name"],
                        description=spell.get("description", ""),
                        icon=f"/cdn/{DDRAGON_VERSION}/img/spell/{spell['image']['full']}",
                        cooldown=spell.get("cooldown"),
                        cost=spell.get("cost"),
                        range=spell.get("range"),
                    )
                )
            except Exception:
                continue

        passive: Optional[ChampionPassive] = None
        if "passive" in champ and champ["passive"] and "image" in champ["passive"]:
            passive = ChampionPassive(
                name=champ["passive"].get("name", ""),
                description=champ["passive"].get("description", ""),
                icon=f"/cdn/{DDRAGON_VERSION}/img/passive/{champ['passive']['image']['full']}",
            )
        
        skins: List[ChampionSkin] = []
        for skin in champ.get("skins", []) or []:
            try:
                skins.append(
                    ChampionSkin(
                        id=f"{champ['id'].lower()}_{skin['num']}",
                        num=skin["num"],
                        name=skin["name"],
                        chromas=skin.get("chromas", False),
                        splash=f"/cdn/img/champion/splash/{champ['id']}_{skin['num']}.jpg",
                        loading=f"/cdn/img/champion/loading/{champ['id']}_{skin['num']}.jpg",
                    )
                )
            except Exception:
                continue

        try:
            info = champ.get("info")
            stats = champ.get("stats")

            return ChampionDetail(
                id=champ["id"],
                key=champ["key"],
                name=champ["name"],
                title=champ.get("title"),
                tags=champ.get("tags", []),
                icon=f"/cdn/{DDRAGON_VERSION}/img/champion/{champ['image']['full']}",
                lore=champ.get("lore") or champ.get("blurb", ""),
                info=ChampionInfo(**info) if isinstance(info, dict) else None,
                stats=ChampionStats(**stats) if isinstance(stats, dict) else None,
                passive=passive,
                abilities=abilities,
                skins=skins
            )
        except Exception:
            return None