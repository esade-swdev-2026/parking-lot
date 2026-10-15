import typer

from parking_lot.parking_functions import free_spaces_in_parking, price_to_pay_for_park

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
