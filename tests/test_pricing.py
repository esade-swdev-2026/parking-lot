import pytest

from parking_lot.pricing import price_with_daily_cap


def test_price_below_daily_cap() -> None:
    assert price_with_daily_cap(60, 0.05) == pytest.approx(3.0)


def test_price_above_daily_cap() -> None:
    assert price_with_daily_cap(600, 0.05) == pytest.approx(20.0)


def test_price_for_two_full_days() -> None:
    assert price_with_daily_cap(2880, 0.05) == pytest.approx(40.0)


def test_price_for_one_day_and_one_hour() -> None:
    assert price_with_daily_cap(1500, 0.05) == pytest.approx(23.0)


def test_custom_daily_cap() -> None:
    assert price_with_daily_cap(600, 0.05, 15.0) == pytest.approx(15.0)


def test_negative_daily_cap() -> None:
    with pytest.raises(ValueError):
        price_with_daily_cap(60, 0.05, -10.0)


def test_negative_minutes() -> None:
    with pytest.raises(ValueError):
        price_with_daily_cap(-5, 0.05)


def test_negative_price_per_minute() -> None:
    with pytest.raises(ValueError):
        price_with_daily_cap(60, -0.05)
