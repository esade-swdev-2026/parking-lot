import typer

app = typer.Typer(help="Terminal Parking Lot Manager")


@app.command()
def main() -> None:
    """Terminal Parking Lot Manager"""


@app.command()
def free(occupied: int, capacity: int = 100) -> None:  # por defecto habra una cap de 100
    if occupied < 0 or occupied > capacity:
        typer.echo("Invalid number of parking spaces", err=True)
        raise typer.Exit(code=1)
    typer.echo(f"{capacity - occupied} free spaces")


if __name__ == "__main__":
    app()
