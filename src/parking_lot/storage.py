import json
from datetime import datetime
from pathlib import Path

STATE_FILE = Path("data/lot.json")


def load_cars(path: Path = STATE_FILE) -> dict[str, datetime]:
    if not path.exists():
        return {}

    data = json.loads(path.read_text(encoding="utf-8"))
    return {plate: datetime.fromisoformat(entry_time) for plate, entry_time in data.items()}


def save_cars(cars: dict[str, datetime], path: Path = STATE_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {plate: entry_time.isoformat() for plate, entry_time in cars.items()}
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
