from datetime import datetime, timedelta
from pathlib import Path

import pytest
from typer.testing import CliRunner

from parking_lot.cli import app
from parking_lot.storage import load_lot, save_lot

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


def test_check_if_car_inside_finds_a_car_saved_by_enter(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    runner.invoke(app, ["enter", "1234ABC", "--lot-file", str(lot_file)])

    result = runner.invoke(app, ["check-if-car-inside", "1234abc", "--lot-file", str(lot_file)])

    assert result.exit_code == 0
    assert "1234ABC is inside the parking lot" in result.stdout


def test_enter_check_and_leave_work_together(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    check = ["check-if-car-inside", "1234ABC", "--lot-file", str(lot_file)]

    assert runner.invoke(app, ["enter", "1234ABC", "--lot-file", str(lot_file)]).exit_code == 0
    assert "1234ABC is inside the parking lot" in runner.invoke(app, check).stdout

    assert runner.invoke(app, ["leave", "1234ABC", "--lot-file", str(lot_file)]).exit_code == 0
    assert "1234ABC is not inside the parking lot" in runner.invoke(app, check).stdout
    assert load_lot(lot_file) == {}


def test_check_if_car_inside_uses_parked_instead_of_the_lot_file(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    runner.invoke(app, ["enter", "1234ABC", "--lot-file", str(lot_file)])

    result = runner.invoke(
        app,
        ["check-if-car-inside", "1234ABC", "--parked", "5678DEF", "--lot-file", str(lot_file)],
    )

    assert result.exit_code == 0
    assert "1234ABC is not inside the parking lot" in result.stdout


@pytest.mark.parametrize(
    "command",
    [
        ["free"],
        ["full"],
        ["check-if-car-inside", "1234ABC"],
        ["enter", "1234ABC"],
        ["leave", "1234ABC"],
    ],
)
def test_commands_report_a_damaged_lot_file_without_a_traceback(
    tmp_path: Path, command: list[str]
) -> None:
    lot_file = tmp_path / "lot.json"
    lot_file.write_text("{not json", encoding="utf-8")

    result = runner.invoke(app, [*command, "--lot-file", str(lot_file)])

    assert result.exit_code == 1
    assert "is not valid JSON" in result.stderr
    assert "Traceback" not in result.output
    assert lot_file.read_text(encoding="utf-8") == "{not json"


def test_leave_shows_the_minutes_and_the_price(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    save_lot(lot_file, {"1234ABC": datetime.now() - timedelta(minutes=60)})

    result = runner.invoke(app, ["leave", "1234ABC", "--lot-file", str(lot_file)])

    assert result.exit_code == 0
    assert "Parked for 60 minutes" in result.stdout
    assert "Price to pay with daily cap: 3.00€" in result.stdout


def test_leave_applies_the_daily_cap(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    save_lot(lot_file, {"1234ABC": datetime.now() - timedelta(hours=10)})

    result = runner.invoke(
        app, ["leave", "1234ABC", "--daily-cap", "15", "--lot-file", str(lot_file)]
    )

    assert result.exit_code == 0
    assert "Price to pay with daily cap: 15.00€" in result.stdout


def test_leave_keeps_the_car_when_the_price_is_invalid(tmp_path: Path) -> None:
    lot_file = tmp_path / "lot.json"
    runner.invoke(app, ["enter", "1234ABC", "--lot-file", str(lot_file)])

    result = runner.invoke(
        app, ["leave", "1234ABC", "--daily-cap", "0", "--lot-file", str(lot_file)]
    )

    assert result.exit_code == 1
    assert "1234ABC" in load_lot(lot_file)
