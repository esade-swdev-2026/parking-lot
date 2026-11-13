from datetime import datetime
from pathlib import Path

from parking_lot.storage import load_cars, save_cars


def test_save_and_load_cars(tmp_path: Path) -> None:
    file = tmp_path / "data" / "lot.json"

    assert load_cars(file) == {}

    cars = {"1234ABC": datetime(2026, 11, 13, 12, 0)}
    save_cars(cars, file)

    assert load_cars(file) == cars
