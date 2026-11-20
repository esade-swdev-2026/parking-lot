import math

from parking_lot.parking_functions import price_to_pay_for_park

DEFAULT_DAILY_CAP = 20.0
MINUTES_PER_DAY = 24 * 60


def price_with_daily_cap(
    minutes: int,
    price_per_minute: float,
    daily_cap: float = DEFAULT_DAILY_CAP,
) -> float:
    """Calculate parking price with a cap for each 24-hour period."""
    if not 0 < daily_cap < math.inf:
        raise ValueError("Daily cap must be greater than zero")

    if minutes < 0:
        raise ValueError("minutes cannot be negative")

    full_day_price = min(price_to_pay_for_park(MINUTES_PER_DAY, price_per_minute), daily_cap)
    full_days, remaining_minutes = divmod(minutes, MINUTES_PER_DAY)
    remaining_price = min(price_to_pay_for_park(remaining_minutes, price_per_minute), daily_cap)

    return full_days * full_day_price + remaining_price
