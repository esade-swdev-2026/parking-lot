from typer.testing import CliRunner

from parking_lot.cli import app

runner = CliRunner()


def test_park_car() -> None:
    result = runner.invoke(app, ["1234ABC"])
    assert result.exit_code == 0
    assert "Vehicle 1234ABC parked successfully." in result.stdout


def test_park_car_with_spaces() -> None:
    result = runner.invoke(app, ["1234ABC", "--spaces", "20"])
    assert result.exit_code == 0
    assert "Total parking spaces: 20" in result.stdout


def test_park_rejects_invalid_spaces() -> None:
    result = runner.invoke(app, ["1234ABC", "--spaces", "0"])
    assert result.exit_code == 1
    assert "The number of parking spaces must be at least 1." in result.stdout
