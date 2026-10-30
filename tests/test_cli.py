import pytest
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


@pytest.mark.parametrize(
    ("arguments", "expected_message"),
    [
        (
            ["check-if-car-inside", "1234ABC", "--parked", "1234ABC,5678DEF"],
            "1234ABC is inside the parking lot",
        ),
        (
            ["check-if-car-inside", "9999ZZZ", "--parked", "1234ABC,5678DEF"],
            "9999ZZZ is not inside the parking lot",
        ),
        (
            ["check-if-car-inside", "1234ABC"],
            "1234ABC is not inside the parking lot",
        ),
    ],
)
def test_check_if_car_inside_reports_where_the_car_is(
    arguments: list[str], expected_message: str
) -> None:
    result = runner.invoke(app, arguments)
    assert result.exit_code == 0
    assert expected_message in result.stdout


def test_check_if_car_inside_rejects_an_empty_plate() -> None:
    result = runner.invoke(app, ["check-if-car-inside", ""])
    assert result.exit_code == 1
    assert "The license plate cannot be empty" in result.stderr


@pytest.mark.parametrize(
    ("arguments", "expected_price"),
    [
        (["price", "60"], "3.00€"),
        (["price", "60", "--price-per-minute", "0.10"], "6.00€"),
        (["price", "0"], "0.00€"),
        (["price", "1"], "0.05€"),
    ],
)
def test_price_shows_the_price_to_pay(arguments: list[str], expected_price: str) -> None:
    result = runner.invoke(app, arguments)
    assert result.exit_code == 0
    assert f"Price to pay for the parking: {expected_price}" in result.stdout


def test_price_rejects_negative_minutes() -> None:
    result = runner.invoke(app, ["price", "--", "-5"])
    assert result.exit_code == 1
    assert "minutes cannot be negative" in result.stderr


def test_price_rejects_minutes_that_are_not_a_number() -> None:
    result = runner.invoke(app, ["price", "abc"])
    assert result.exit_code == 2
