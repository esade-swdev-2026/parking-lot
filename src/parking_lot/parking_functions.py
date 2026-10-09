from datetime import datetime

DATA_FILE = "parking.txt"
HOURS_PER_DAY = 24
MINUTES_PER_HOUR = 60


def parking_is_full(occupied: int, capacity: int) -> bool:
    return occupied >= capacity


def car_is_inside(cars: dict[str, datetime], plate: str) -> bool:
    return plate in cars


def car_enter_parking(
    cars: dict[str, datetime], plate: str, entry_time: datetime, capacity: int
) -> dict[str, datetime]:
    if parking_is_full(len(cars), capacity):
        raise ValueError("the parking lot is full")
    if car_is_inside(cars, plate):
        raise ValueError(f"{plate} is already inside")
    new_cars = dict(cars)
    new_cars[plate] = entry_time
    return new_cars


def car_exists_parking(cars: dict[str, datetime], plate: str) -> dict[str, datetime]:
    if len(cars) == 0:
        raise ValueError("the parking lot is empty")
    if not car_is_inside(cars, plate):
        raise ValueError(f"{plate} is not inside")
    new_cars = dict(cars)
    del new_cars[plate]
    return new_cars


def minutes_parked(entry_time: datetime, exit_time: datetime) -> int:
    if exit_time < entry_time:
        raise ValueError("exit time cannot be before entry time")
    days = exit_time.day - entry_time.day
    hours = exit_time.hour - entry_time.hour
    minutes = exit_time.minute - entry_time.minute
    return days * HOURS_PER_DAY * MINUTES_PER_HOUR + hours * MINUTES_PER_HOUR + minutes


def price_to_pay_for_park(minutes: int, price_per_minute: float) -> float:
    if minutes < 0:
        raise ValueError("minutes cannot be negative")
    return minutes * price_per_minute
