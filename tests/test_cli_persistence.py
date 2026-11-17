from pathlib import Path

from typer.testing import CliRunner

from parking_lot.cli import app
from parking_lot.storage import load_lot

runner = CliRunner()


def test_enter_saves_the_car_in_the_lot_file(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"

    result = runner.invoke(app, ["enter", "1234abc", "--lot-file", str(lot_file)])

    assert result.exit_code == 0
    assert "1234ABC" in load_lot(lot_file)


def test_enter_fails_when_the_car_is_already_inside(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    runner.invoke(app, ["enter", "1234ABC", "--lot-file", str(lot_file)])

    result = runner.invoke(app, ["enter", "1234ABC", "--lot-file", str(lot_file)])

    assert result.exit_code == 1


def test_enter_fails_when_the_lot_is_full(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    runner.invoke(app, ["enter", "1234ABC", "--capacity", "1", "--lot-file", str(lot_file)])

    result = runner.invoke(
        app, ["enter", "5678XYZ", "--capacity", "1", "--lot-file", str(lot_file)]
    )

    assert result.exit_code == 1
    assert "5678XYZ" not in load_lot(lot_file)


def test_leave_removes_the_car_from_the_lot_file(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    runner.invoke(app, ["enter", "1234ABC", "--lot-file", str(lot_file)])

    result = runner.invoke(app, ["leave", "1234ABC", "--lot-file", str(lot_file)])

    assert result.exit_code == 0
    assert load_lot(lot_file) == {}


def test_leave_fails_when_the_car_is_not_inside(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"

    result = runner.invoke(app, ["leave", "1234ABC", "--lot-file", str(lot_file)])

    assert result.exit_code == 1


def test_free_counts_the_cars_in_the_lot_file(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    runner.invoke(app, ["enter", "1234ABC", "--lot-file", str(lot_file)])

    result = runner.invoke(app, ["free", "--capacity", "3", "--lot-file", str(lot_file)])

    assert result.exit_code == 0
    assert "2 free spaces" in result.output


def test_full_reads_the_lot_file(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    runner.invoke(app, ["enter", "1234ABC", "--capacity", "1", "--lot-file", str(lot_file)])

    result = runner.invoke(app, ["full", "--capacity", "1", "--lot-file", str(lot_file)])

    assert result.exit_code == 0
    assert "The parking is full" in result.output
