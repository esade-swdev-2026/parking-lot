from datetime import datetime

import pytest

import parking_lot.parking_functions

NINE = datetime(2026, 10, 9, 9, 0)
TEN = datetime(2026, 10, 9, 10, 0)


def test_parking_is_not_full_with_free_spaces() -> None:
    assert parking_lot.parking_functions.parking_is_full(99, 100) is False


def test_parking_is_full_when_exactly_at_capacity() -> None:
    assert parking_lot.parking_functions.parking_is_full(100, 100) is True


def test_car_is_inside_finds_a_parked_car() -> None:
    assert parking_lot.parking_functions.car_is_inside({"1234ABC": NINE}, "1234ABC") is True


def test_car_is_inside_rejects_a_missing_plate() -> None:
    assert parking_lot.parking_functions.car_is_inside({"1234ABC": NINE}, "9999ZZZ") is False


def test_car_enter_parking_adds_the_car() -> None:
    cars = parking_lot.parking_functions.car_enter_parking({}, "1234ABC", NINE, 100)
    assert cars == {"1234ABC": NINE}


def test_car_enter_parking_rejects_when_full() -> None:
    with pytest.raises(ValueError):
        parking_lot.parking_functions.car_enter_parking({"1234ABC": NINE}, "5678DEF", TEN, 1)


def test_car_enter_parking_rejects_the_same_car_twice() -> None:
    with pytest.raises(ValueError):
        parking_lot.parking_functions.car_enter_parking({"1234ABC": NINE}, "1234ABC", TEN, 100)


def test_car_leaves_parking_removes_the_car() -> None:
    cars = parking_lot.parking_functions.car_leaves_parking({"1234ABC": NINE}, "1234ABC")
    assert cars == {}


def test_car_leaves_parking_rejects_when_empty() -> None:
    with pytest.raises(ValueError):
        parking_lot.parking_functions.car_leaves_parking({}, "1234ABC")


def test_car_leaves_parking_rejects_a_missing_car() -> None:
    with pytest.raises(ValueError):
        parking_lot.parking_functions.car_leaves_parking({"1234ABC": NINE}, "9999ZZZ")


def test_minutes_parked_one_hour() -> None:
    assert parking_lot.parking_functions.minutes_parked(NINE, TEN) == 60


def test_minutes_parked_overnight() -> None:
    entry = datetime(2026, 10, 9, 23, 0)
    exit_ = datetime(2026, 10, 10, 1, 0)
    assert parking_lot.parking_functions.minutes_parked(entry, exit_) == 120


def test_minutes_parked_rejects_exit_before_entry() -> None:
    with pytest.raises(ValueError):
        parking_lot.parking_functions.minutes_parked(TEN, NINE)


def test_price_to_pay_for_one_hour() -> None:
    assert parking_lot.parking_functions.price_to_pay_for_park(60, 0.05) == pytest.approx(3.0)


def test_price_to_pay_for_zero_minutes() -> None:
    assert parking_lot.parking_functions.price_to_pay_for_park(0, 0.05) == 0.0


def test_price_to_pay_rejects_negative_minutes() -> None:
    with pytest.raises(ValueError):
        parking_lot.parking_functions.price_to_pay_for_park(-5, 0.05)


def test_free_spaces_with_some_cars() -> None:
    assert parking_lot.parking_functions.free_spaces_in_parking(30, 100) == 70


def test_free_spaces_rejects_more_cars_than_capacity() -> None:
    with pytest.raises(ValueError):
        parking_lot.parking_functions.free_spaces_in_parking(120, 100)
