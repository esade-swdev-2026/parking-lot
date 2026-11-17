from datetime import datetime
from pathlib import Path

from parking_lot.storage import load_lot, save_lot


def test_load_lot_returns_an_empty_lot_when_the_file_does_not_exist(tmp_path: Path) -> None:
    assert load_lot(tmp_path / "lot.json") == {}


def test_save_lot_then_load_lot_returns_the_same_cars(tmp_path: Path) -> None:
    path = tmp_path / "lot.json"
    cars = {"1234ABC": datetime(2026, 11, 20, 9, 30), "5678XYZ": datetime(2026, 11, 20, 10, 0)}

    save_lot(path, cars)

    assert load_lot(path) == cars


def test_save_lot_creates_the_folder_when_it_does_not_exist(tmp_path: Path) -> None:
    path = tmp_path / "data" / "lot.json"

    save_lot(path, {"1234ABC": datetime(2026, 11, 20, 9, 30)})

    assert path.exists()
