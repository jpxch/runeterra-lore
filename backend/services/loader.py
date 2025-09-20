import json
from pathlib import Path
from typing import Any

def load_json(path: Path) -> Any:
    try:
        with open(path, encoding="utf-8") as f:
            data = f.read().strip()
            return json.loads(data) if data else []
    except FileNotFoundError:
            return []