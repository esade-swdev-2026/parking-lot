import json
from datetime import datetime
from pathlib import Path

DEFAULT_LOT_FILE = Path("data/lot.json")


class LotFileError(ValueError):
    """The saved parking lot file cannot be read or written."""


def load_lot(path: Path) -> dict[str, datetime]:
    if not path.exists():
        return {}

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise LotFileError(f"Cannot read {path}: {error.strerror}") from error
    except ValueError as error:
        raise LotFileError(f"{path} is not valid JSON. Fix or delete the file.") from error

    if not isinstance(raw, dict):
        raise LotFileError(f"{path} must contain license plates and entry times.")

    try:
        return {plate: datetime.fromisoformat(entry) for plate, entry in raw.items()}
    except (TypeError, ValueError) as error:
        raise LotFileError(f"{path} contains an invalid entry time.") from error


def save_lot(path: Path, cars: dict[str, datetime]) -> None:
    raw = {plate: entry.isoformat() for plate, entry in cars.items()}
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
    except OSError as error:
        raise LotFileError(f"Cannot write {path}: {error.strerror}") from error
