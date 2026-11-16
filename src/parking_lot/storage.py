import json
from datetime import datetime
from pathlib import Path

DEFAULT_LOT_FILE = Path("data/lot.json")


def load_lot(path: Path) -> dict[str, datetime]:
    if not path.exists():
        return {}
    raw = json.loads(path.read_text())
    return {plate: datetime.fromisoformat(entry) for plate, entry in raw.items()}


def save_lot(path: Path, cars: dict[str, datetime]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = {plate: entry.isoformat() for plate, entry in cars.items()}
    path.write_text(json.dumps(raw, indent=2))
