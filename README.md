# Parking-lot

Parking-lot is a parking lot staff, to help  manage the daily activity of a parking lot from the terminal. With it, staff will be able to register when each car enters and leaves, calculate how much each driver has to pay based on the time parked, and check at any moment how many free spaces are left. 

## I/O

All I/O lives in `free()` in `src/parking_lot/cli.py`: two `typer.echo` calls (the result and the error message) and one `raise typer.Exit(code=1)`. No files are read or written. The free-spaces calculation is currently mixed with this I/O inside the same function.

## Pure functions to test

1. `parking_is_full` — whether the parking lot is full
2. `car_is_inside` — whether a car is inside
3. `car_enter_parking` — next state when a car enters
4. `car_leaves_parking` — next state when a car leaves
5. `minutes_parked` — minutes between entry and exit
6. `price_to_pay_for_park` — price to pay

## Install

```
uv sync
```

This creates a virtual environment and installs everything, including the development
tools, from `uv.lock` — the committed file that pins exact versions so every teammate
and CI resolve the same ones. When you change a dependency in `pyproject.toml`, run
`uv lock` and commit the updated `uv.lock`; CI fails if the two disagree.

## Run

```
uv run parking-lot --help
uv run parking-lot free 30
uv run parking-lot free 30 --capacity 50
```

## Develop

```
uv run ruff check .          # lint
uv run ruff format .         # format (CI runs `--check` and fails on a diff)
uv run mypy src tests        # types
uv run pytest                # tests
```

These four commands are exactly what `.github/workflows/check.yml` runs on every push.
If they pass here, CI passes.

## Layout

```
src/parking_lot/          your package — importable, installable, not just a script
  cli.py          the typer command-line interface
  __main__.py     lets `python -m app` work
tests/            pytest tests, mirroring src/
pyproject.toml    dependencies and tool configuration — the single source of truth
```
