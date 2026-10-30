from typer.testing import CliRunner

from parking_lot.cli import app

runner = CliRunner()


def test_free_shows_the_free_spaces() -> None:
    result = runner.invoke(app, ["free", "30"])
    assert result.exit_code == 0
    assert "70 free spaces" in result.stdout


def test_free_rejects_more_cars_than_capacity() -> None:
    result = runner.invoke(app, ["free", "120"])
    assert result.exit_code == 1


def test_check_if_car_inside_finds_a_parked_car() -> None:
    result = runner.invoke(app, ["check-if-car-inside", "1234ABC", "--parked", "1234ABC,5678DEF"])
    assert result.exit_code == 0
    assert "1234ABC is inside the parking lot" in result.stdout


def test_check_if_car_inside_reports_a_missing_car() -> None:
    result = runner.invoke(app, ["check-if-car-inside", "9999ZZZ", "--parked", "1234ABC,5678DEF"])
    assert result.exit_code == 0
    assert "9999ZZZ is not inside the parking lot" in result.stdout


def test_check_if_car_inside_handles_an_empty_parking() -> None:
    result = runner.invoke(app, ["check-if-car-inside", "1234ABC"])
    assert result.exit_code == 0
    assert "1234ABC is not inside the parking lot" in result.stdout


def test_check_if_car_inside_rejects_an_empty_plate() -> None:
    result = runner.invoke(app, ["check-if-car-inside", ""])
    assert result.exit_code == 1
    assert "The license plate cannot be empty" in result.stderr
