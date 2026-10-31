from datetime import datetime

ANY_YEAR = 2000
ANY_MONTH = 1
ANY_DAY = 1
SECONDS_PER_MINUTE = 60


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


def car_leaves_parking(cars: dict[str, datetime], plate: str) -> dict[str, datetime]:
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
    parked_time = exit_time - entry_time
    return int(parked_time.total_seconds() // SECONDS_PER_MINUTE)


def price_to_pay_for_park(minutes: int, price_per_minute: float) -> float:
    if minutes < 0:
        raise ValueError("minutes cannot be negative")
    if price_per_minute < 0:
        raise ValueError("price per minute cannot be negative")
    return minutes * price_per_minute


def validate_occupied_spaces(occupied: int, capacity: int) -> None:
    if occupied < 0 or occupied > capacity:
        raise ValueError("Invalid number of parking spaces")


def free_spaces_in_parking(occupied: int, capacity: int) -> int:
    validate_occupied_spaces(occupied, capacity)
    return capacity - occupied


def parking_is_full(occupied: int, capacity: int) -> bool:
    validate_occupied_spaces(occupied, capacity)
    return occupied >= capacity


def time_of_day(hour: int, minute: int) -> datetime:
    return datetime(ANY_YEAR, ANY_MONTH, ANY_DAY, hour, minute)
