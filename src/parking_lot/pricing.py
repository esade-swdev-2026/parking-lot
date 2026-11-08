from parking_lot.parking_functions import price_to_pay_for_park

DEFAULT_DAILY_CAP = 20.0


def price_with_daily_cap(
    minutes: int,
    price_per_minute: float,
    daily_cap: float = DEFAULT_DAILY_CAP,
) -> float:
    """Calculate parking price with a cap for each 24-hour period."""
    if daily_cap <= 0:
        raise ValueError("Daily cap must be greater than zero")

    if minutes < 0 or price_per_minute < 0:
        return price_to_pay_for_park(minutes, price_per_minute)

    full_days, remaining_minutes = divmod(minutes, 1440)

    full_day_price = min(
        price_to_pay_for_park(1440, price_per_minute),
        daily_cap,
    )
    remaining_price = min(
        price_to_pay_for_park(remaining_minutes, price_per_minute),
        daily_cap,
    )

    return full_days * full_day_price + remaining_price
