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


@pytest.mark.parametrize(
    ("arguments", "expected_message"),
    [
        (["full", "100"], "The parking is full"),
        (["full", "99"], "There are free spaces"),
        (["full", "0"], "There are free spaces"),
        (["full", "50", "--capacity", "50"], "The parking is full"),
    ],
)
def test_full_says_if_the_parking_is_full(arguments: list[str], expected_message: str) -> None:
    result = runner.invoke(app, arguments)
    assert result.exit_code == 0
    assert expected_message in result.stdout


@pytest.mark.parametrize(
    "arguments",
    [
        ["full", "120"],
        ["full", "--", "-1"],
    ],
)
def test_full_rejects_an_impossible_numer_of_cars(arguments: list[str]) -> None:
    result = runner.invoke(app, arguments)
    assert result.exit_code == 1
    assert "Invalid number of parking spaces" in result.stderr


def test_full_rejects_cars_that_are_not_a_number() -> None:
    result = runner.invoke(app, ["full", "abc"])
    assert result.exit_code == 2


@pytest.mark.parametrize(
    ("arguments", "expected_minutes", "expected_price"),
    [
        (["stay", "9", "40", "11", "15"], 95, "4.75€"),
        (["stay", "9", "0", "9", "0"], 0, "0.00€"),
        (["stay", "0", "0", "23", "59"], 1439, "71.95€"),
        (["stay", "9", "0", "10", "0", "--price-per-minute", "0.10"], 60, "6.00€"),
    ],
)
def test_stay_shows_the_minutes_and_the_price(
    arguments: list[str], expected_minutes: int, expected_price: str
) -> None:
    result = runner.invoke(app, arguments)
    assert result.exit_code == 0
    assert f"Parked for {expected_minutes} minutes" in result.stdout
    assert f"Price to pay for the parking: {expected_price}" in result.stdout


@pytest.mark.parametrize(
    ("arguments", "expected_error"),
    [
        (["stay", "11", "0", "9", "0"], "exit time cannot be before entry time"),
        (["stay", "24", "0", "10", "0"], "hour"),
        (["stay", "9", "60", "10", "0"], "minute"),
    ],
)
def test_stay_rejects_impossible_times(arguments: list[str], expected_error: str) -> None:
    result = runner.invoke(app, arguments)
    assert result.exit_code == 1
    assert expected_error in result.stderr


@pytest.mark.parametrize(
    "arguments",
    [
        ["stay", "9", "abc", "10", "0"],
        ["stay", "9", "40"],
    ],
)
def test_stay_rejects_wrong_arguments(arguments: list[str]) -> None:
    result = runner.invoke(app, arguments)
    assert result.exit_code == 2
