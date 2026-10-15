import typer

import parking_lot.parking_functions

app = typer.Typer(help="Terminal Parking Lot Manager")


@app.callback()
def main() -> None:
    """Terminal Parking Lot Manager"""


@app.command()  
def free(occupied: int, capacity: int = 100) -> None:
    try:
        spaces = parking_lot.parking_functions.free_spaces_in_parking(occupied, capacity)  # noqa: F821
    except ValueError as error:
        typer.echo(str(error), err=True)
        raise typer.Exit(code=1) from error
    typer.echo(f"{spaces} free spaces")
