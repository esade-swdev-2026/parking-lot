import typer

from parking_lot.parking_functions import (
    free_spaces_in_parking,
    minutes_parked,
    parking_is_full,
    price_to_pay_for_park,
    time_of_day,
)

app = typer.Typer(help="Terminal Parking Lot Manager")

DEFAULT_CAPACITY = 100
DEFAULT_PRICE_PER_MINUTE = 0.05


@app.callback()
def main() -> None:
    """Terminal Parking Lot Manager"""


@app.command()
def free(occupied: int, capacity: int = DEFAULT_CAPACITY) -> None:
    try:
        spaces = free_spaces_in_parking(occupied, capacity)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    typer.echo(f"{spaces} free spaces")


@app.command()
def price(minutes: int, price_per_minute: float = DEFAULT_PRICE_PER_MINUTE) -> None:
    try:
        total = price_to_pay_for_park(minutes, price_per_minute)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    typer.echo(f"Price to pay for the parking: {total:.2f}€")


@app.command()
def full(occupied: int, capacity: int = DEFAULT_CAPACITY) -> None:
    try:
        is_full = parking_is_full(occupied, capacity)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    if is_full:
        typer.echo("The parking is full")
    else:
        typer.echo("There are free spaces")


@app.command()
def stay(
    entry_hour: int,
    entry_minute: int,
    exit_hour: int,
    exit_minute: int,
    price_per_minute: float = DEFAULT_PRICE_PER_MINUTE,
) -> None:
    try:
        entry = time_of_day(entry_hour, entry_minute)
        exit_ = time_of_day(exit_hour, exit_minute)
        minutes = minutes_parked(entry, exit_)
        total = price_to_pay_for_park(minutes, price_per_minute)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    typer.echo(f"Parked for {minutes} minutes")
    typer.echo(f"Price to pay for the parking: {total:.2f}€")


@app.command()
def check_if_car_inside(plate: str, parked: str = "") -> None:
    if not plate:
        typer.echo("The license plate cannot be empty", err=True)
        raise typer.Exit(code=1)

    cars = parked.split(",") if parked else []

    if plate in cars:
        typer.echo(f"{plate} is inside the parking lot")
    else:
        typer.echo(f"{plate} is not inside the parking lot")
