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


def test_free_uses_a_custom_capacity() -> None:
    result = runner.invoke(app, ["free", "30", "--capacity", "50"])
    assert result.exit_code == 0
    assert "20 free spaces" in result.stdout
