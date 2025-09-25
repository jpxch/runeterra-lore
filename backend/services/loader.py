from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

import httpx

from backend.config import settings
from backend.models.champion import ChampionSummary, ChampionDetail

_CHAMPION_FIXTURE = settings.data_dir / "champions.json"
_CHAMPION_CACHE = settings.cache_dir / "champions.cache.json"
_VERSION_CACHE = settings.cache_dir / "version.txt"

class ChampionRepository:
    """Unified data access: live -> cache -> fixture."""
    
    def __init__(self) -> None:
        self._by_id: Dict[str, ChampionDetail] = {}

    # -------- Public API --------
    def list_summaries(self, search: Optional[str] = None) -> List[ChampionSummary]:
        data = self._ensure_loaded()
        items = [ChampionSummary.model_validate(c) for c in data.values()]
        if search:
            q = search.lower()
            items = [s for s in items if q in s.name.lower() or (s.region or "").lower().find(q) >= 0]
        return sorted(items, key=lambda s: s.name.lower())
    
    def get_detail(self, champ_id: str) -> Optional[ChampionDetail]:
        data = self._ensure_loaded()
        return data.get(champ_id)

    # -------- Internal plumbing --------
    def _ensure_loaded(self) -> Dict[str, ChampionDetail]:
        if self._by_id:
            return self._by_id

        live = self._try_live()
        if live:
            self._by_id = live
            self._write_cache(live)
            return self._by_id
        
        cached = self._try_cache()
        if cached:
            self._by_id = cached
            return self._by_id

        fixture = self._try_fixtures()
        self._by_id = fixtures
        return self._by_id

    def _try_live(self) -> Optional[Dict[str, ChampionDetail]]:
        """Fetch latest champion list from Data Dragon."""
        try:
            with httpx.Client(timeout=10.0) as client:
                # Fetch latest patch version
                versions_url = "https://ddragon.leagueoflegends.com/api/versions.json"
                version_resp = client.get(versions_url)
                version_resp.raise_for_status()
                versions = version_resp.json()
                if not versions:
                    return None
                latest_version = versions[0]

                # cache version string
                _VERSION_CACHE.write_text(latest_version, encoding="utf-8")

                # Fetch champions manifest
                champ_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/{settings.riot_defatult_locale}/champion.json"
                resp = client.get(champs_url)
                resp.raise_for_status()
                payload = resp.json()

            return self._normalize_ddragon(payload)
        except Exception:
            return None

    def _try_cache(self) -> Optional[Dict[str, ChampionDetail]]:
        try:
            if not _CHAMPIONS_CACHE.exists():
                return None
            if self._expired(_CHAMPION_CACHE):
                return None
            data = json.loads(_CHAMPION_CACHE.read_text(encoding="utf-8"))
            return {cid: ChampionDetail.model_validate(c) for cid, c in data.items()}
        except Exception:
            return None

    def _write_cache(self, date: Dict[str, ChampionDetail]) -> None:
        try:
            serializable = {k: v.model_dump() for k, v in data.items()}
            _CHAMPION_CACHE.write_text(json.dumps(serializable, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _try_fixtures(self) -> Dict[str, ChampionDetail]:
        if not _CHAMPION_FIXTURE.exists():
            return {}
        try:
            raw = json.loads(_CHAMPIONS_FIXTURE.read_text(encoding="utf-8"))
            return {c["id"]: ChampionDetail.model_validate(c) for c in raw}
        except Exception:
            return {}

    def _normalize_ddragon(self, raw) -> Dict[str, ChampionDetail]:
        """Transform ddragon schema into ChampionDetail objects."""
        out: Dict[str, ChampionDetail] = {}
        data = raw.get("data", {})
        for cid, champ in data.items():
            try:
                detail = ChampionDetail(
                    id=champ["id"].lower(),
                    name=champ["name"],
                    region=None,
                    icon=f"/cdn/{champ.get('image', {}).get('full')}" if "image" in champ else None,
                    roles=champ.get("tags", []),
                    lore=champ.get("blurb"),
                    abilities={},
                    skins=[s.get("name") for s in champ.get("skins", [])] if "skins" in champ else []
                )
                out[detail.id] = detail
            except Exception:
                continue
        return out

    def _expired(self, path: Path) -> bool:
        try:
            mtime = path.stat().st_mtime
            return (time.time() - mtime) > 86400
        except Exception:
            return True


# Singleton accessor
champions_repo = ChampionRepository()