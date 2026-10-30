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


@app.command(help="Show the number of available parking spaces.")
def free(
    occupied: int = typer.Argument(help="Number of currently occupied parking spaces."),
    capacity: int = typer.Option(DEFAULT_CAPACITY, help="Maximum number of parking spaces."),
) -> None:
    try:
        spaces = free_spaces_in_parking(occupied, capacity)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    typer.echo(f"{spaces} free spaces")


@app.command(help="Calculate the parking price for a given number of minutes.")
def price(
    minutes: int = typer.Argument(help="Number of minutes the car was parked."),
    price_per_minute: float = typer.Option(
        DEFAULT_PRICE_PER_MINUTE, help="Parking price per minute in euros."
    ),
) -> None:
    try:
        total = price_to_pay_for_park(minutes, price_per_minute)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    typer.echo(f"Price to pay for the parking: {total:.2f}€")


@app.command(help="Check whether the parking lot is full.")
def full(
    occupied: int = typer.Argument(help="Number of currently occupied parking spaces."),
    capacity: int = typer.Option(DEFAULT_CAPACITY, help="Maximum number of parking spaces."),
) -> None:
    try:
        is_full = parking_is_full(occupied, capacity)
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    if is_full:
        typer.echo("The parking is full")
    else:
        typer.echo("There are free spaces")


@app.command(help="Calculate the parking duration and total price.")
def stay(
    entry_hour: int = typer.Argument(help="Hour when the car entered (0-23)."),
    entry_minute: int = typer.Argument(help="Minute when the car entered (0-59)."),
    exit_hour: int = typer.Argument(help="Hour when the car left (0-23)."),
    exit_minute: int = typer.Argument(help="Minute when the car left (0-59)."),
    price_per_minute: float = typer.Option(
        DEFAULT_PRICE_PER_MINUTE, help="Parking price per minute in euros."
    ),
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


@app.command(help="Check whether a license plate is in the parking lot.")
def check_if_car_inside(
    plate: str = typer.Argument(help="License plate to look for in the parking lot."),
    parked: str = typer.Option("", help="Comma-separated list of parked license plates."),
) -> None:
    if not plate:
        typer.echo("The license plate cannot be empty", err=True)
        raise typer.Exit(code=1)

    cars = parked.split(",") if parked else []

    if plate in cars:
        typer.echo(f"{plate} is inside the parking lot")
    else:
        typer.echo(f"{plate} is not inside the parking lot")
