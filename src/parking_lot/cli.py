import typer

app = typer.Typer(help="A simple command-line application for managing a parking lot.")


@app.command()
def park(plate: str = typer.Argument(..., help="License plate of the vehicle."),
    spaces: int = typer.Option(10, "--spaces", help="Total number of parking spaces."),
) -> None:
    """Park a car in the parking lot."""
    if spaces < 1:
        typer.echo("The number of parking spaces must be at least 1.", err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Vehicle {plate} parked successfully.")
    typer.echo(f"Total parking spaces: {spaces}")


if __name__ == "__main__":
    app()
