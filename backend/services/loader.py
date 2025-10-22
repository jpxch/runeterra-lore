import json
import requests
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from backend.models.champion import (
    ChampionSummary,
    ChampionDetail,
    ChampionInfo,
    ChampionStats,
    ChampionAbility,
    ChampionPassive,
)
from backend.models.skin import Skin, ChampionSkinSummary
from backend.models.region import RegionSummary, RegionDetail
from backend.core.config import settings

logger = logging.getLogger("ddragon")
logger.setLevel(logging.INFO)


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
    cache_file = settings.cache_dir / "ddragon_version.json"
    if cache_file.exists():
        try:
            cached = json.loads(cache_file.read_text())
            if isinstance(cached, dict) and "version" in cached:
                return cached["version"]
        except Exception:
            pass

    try:
        r = requests.get(VERSIONS_URL, timeout=5)
        r.raise_for_status()
        versions = r.json()
        if isinstance(versions, list) and versions:
            latest = versions[0]
            cache_file.write_text(json.dumps({"version": latest}))
            logger.info(f"Using DDragon version {latest}")
            return latest
    except Exception as e:
        logger.warning(f"Failed to fetch DDragon version: {e}")

    return "14.18.1"


DDRAGON_VERSION = get_latest_version()
DDRAGON_BASE = f"https://ddragon.leagueoflegends.com/cdn/{DDRAGON_VERSION}/data/en_US"


def fetch_ddragon_data(endpoint: str) -> Optional[dict]:
    """Fetch JSON from ddragon, return None if request fails."""
    cache_path = settings.cache_dir / f"{endpoint.replace('/', '_')}.json"
    if cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text())
            if cached:
                return cached
        except Exception:
            logger.warning(f"Cache file {cache_path.name} corrupt, refetching.")

    url = f"{DDRAGON_BASE}/{endpoint}"
    try:
        logger.info(f"Fetching {url}")
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        data = r.json()
        cache_path.write_text(json.dumps(data))
        return data
    except Exception as e:
        logger.warning(f"DDragon request failed for {endpoint}: {e}")
        return None


CHAMPIONS_FILE = settings.data_dir / "champions.json"


class ChampionRepository:
    """Repository for champion data with ddragon + fallback."""

    def __init__(self) -> None:
        self._by_id: Dict[str, dict] = self._load()

    def _load(self) -> Dict[str, dict]:
        """Load all champions from cache or fetch fresh from DDragon."""
        cached = load_json(CHAMPIONS_FILE)
        if isinstance(cached, dict) and cached:
            logger.info("Loaded champions from local cache.")
            return cached

        raw = fetch_ddragon_data("champion.json")
        if raw and "data" in raw:
            champions = raw["data"]
            save_json(CHAMPIONS_FILE, champions)
            logger.info(f"Pulled {len(champions)} champions from DDragon.")
            return champions

        logger.warning("No champion data available.")
        return {}

    def list_summaries(self, search: Optional[str] = None) -> List[ChampionSummary]:
        out: List[ChampionSummary] = []
        for champ in self._by_id.values():
            if search and search.lower() not in champ["name"].lower():
                continue
            try:
                out.append(
                    ChampionSummary(
                        id=champ["id"],
                        key=champ["key"],
                        name=champ["name"],
                        title=champ["title"],
                        tags=champ.get("tags", []),
                        icon=f"/cdn/{DDRAGON_VERSION}/img/champion/{champ['image']['full']}",
                    )
                )
            except Exception:
                continue
        return sorted(out, key=lambda c: c.name.lower())

    def get_detail(self, champ_id: str) -> Optional[ChampionDetail]:
        """Return a single ChampionDetail by ID, or None if not found."""
        champ_key = next(
            (cid for cid in self._by_id.keys() if cid.lower() == champ_id.lower()), None
        )
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

        skins: List[ChampionSkinSummary] = []
        for skin in champ.get("skins", []) or []:
            try:
                skins.append(
                    ChampionSkinSummary(
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
                skins=skins,
            )
        except Exception:
            return None


champions_repo = ChampionRepository()

SKINS_FILE = settings.data_dir / "skins.json"


class SkinRepository:
    """Repository for champion skin from DDragon + local cache."""

    def __init__(self) -> None:
        print("[FSL] Initializing SkinRepository")
        self._skins: List[Skin] = self._load()

    def _load(self) -> List[Skin]:
        """Fetch all skins from local JSON or rebuild from champion data."""
        cached = load_json(SKINS_FILE)
        print(
            f"[FSL] Cached skins: type={type(cached)}, length={len(cached) if isinstance(cached, list) else 'N/A'}"
        )

        if not isinstance(cached, list) or not cached:
            print("[FSL] Building skins repository from champions data...")
            all_skins: List[dict] = []

            print(f"[FSL] Champions in repo: {len(champions_repo._by_id)}")

            for champ_id in champions_repo._by_id.keys():
                detailed = fetch_ddragon_data(f"champion/{champ_id}.json")
                if (
                    not detailed
                    or "data" not in detailed
                    or champ_id not in detailed["data"]
                ):
                    continue
                champ = detailed["data"][champ_id]
                for skin in champ.get("skins", []) or []:
                    all_skins.append(
                        {
                            "id": f"{champ['id'].lower()}_{skin['num']}",
                            "champion_id": champ["id"],
                            "name": skin["name"],
                            "num": skin["num"],
                            "chromas": skin.get("chromas", False),
                            "splash": f"/cdn/img/champion/splash/{champ['id']}_{skin['num']}.jpg",
                            "loading": f"/cdn/img/champion/loading/{champ['id']}_{skin['num']}.jpg",
                        }
                    )
            print(f"[FSL] Built {len(all_skins)} skins.")
            save_json(SKINS_FILE, all_skins)
            return [Skin(**s) for s in all_skins]

        print(f"[FSL] Using cached {len(cached)} skins.")
        return [Skin(**s) for s in cached]

    def list_all(self) -> List[Skin]:
        """Return all skins as model objects."""
        return sorted(self._skins, key=lambda s: s.name.lower())

    def get(self, skin_id: str) -> Optional[Skin]:
        """Return a single skin by ID, or None if not found."""
        for s in self._skins:
            if s.id.lower() == skin_id.lower():
                return s
        return None


skins_repo = SkinRepository()

REGIONS_FILE = settings.data_dir / "regions.json"


class RegionRepository:
    """Repository for region data from canonical JSON."""

    def __init__(self) -> None:
        self._regions = self._load()

    def _load(self) -> List[dict]:
        data = load_json(REGIONS_FILE)
        return data if isinstance(data, list) else []

    def list_all(self) -> List[RegionSummary]:
        """Return all regions as RegionSummary models."""
        return [RegionSummary(**r) for r in self._regions]

    def get(self, region_id: str) -> Optional[RegionDetail]:
        """Return a single region by ID, or None if not found."""
        for r in self._regions:
            if r.get("id", "").lower() == region_id.lower():
                return RegionDetail(**r)
        return None


regions_repo = RegionRepository
