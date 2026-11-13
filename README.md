# Parking-lot

Parking-lot is a command-line tool for parking lot staff, to help them manage the daily activity of a parking lot from the terminal. With it, staff can check how many free spaces are left and calculate how much a driver has to pay based on the time parked. The core also handles cars entering and leaving, ready to be connected to new commands.

## I/O

Console input and output are handled in `src/parking_lot/cli.py` with Typer.
The commands display results with `typer.echo` and report errors with
`typer.Exit(code=1)`.

The `enter` and `leave` commands use `src/parking_lot/storage.py` to read and
write the parking state in `data/lot.json`. Each license plate is stored
with its entry time. The `data/` folder is ignored by Git.

Validation and calculations live in the parking functions. These functions
can raise `ValueError`, which the commands catch and show as a clear message.

## Pure functions to test

1. `free_spaces_in_parking` — free spaces left
2. `parking_is_full` — whether the parking lot is full
3. `car_is_inside` — whether a car is inside
4. `car_enter_parking` — next state when a car enters
5. `car_leaves_parking` — next state when a car leaves
6. `minutes_parked` — minutes between entry and exit
7. `price_to_pay_for_park` — price to pay
8. `time_of_day` — a time of day from an hour and a minute

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
uv run parking-lot price 60 
uv run parking-lot price 60 --price-per-minute 0.10
uv run parking-lot full 100
uv run parking-lot stay 9 40 11 15
uv run parking-lot check-if-car-inside 1234ABC --parked "1234ABC,5678DEF"
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
  parking_functions.py
  __main__.py     lets `python -m app` work
tests/            pytest tests, mirroring src/
pyproject.toml    dependencies and tool configuration — the single source of truth
```


## Run with Docker

Start Docker and run these commands from the project folder.

### Build the image

If this branch already contains the Dockerfile from PR #6, build with:

```bash
docker build -t parking-lot:persistence .
```

If this branch does not have the Dockerfile yet, use this option instead:

```bash
git fetch origin add-dockerfile
git show FETCH_HEAD:Dockerfile | docker build -t parking-lot:persistence -f - .
```

This uses the Dockerfile from PR #6 with the code in your current folder.

Show the available commands:

```bash
docker run --rm parking-lot:persistence --help
```

### Check persistence between containers

The app saves its state in `/app/data/lot.json` inside the container.
Use the same named volume for each command.

Register a car:

```bash
docker run --rm -v parking-lot-lab16-test:/app/data parking-lot:persistence enter 1234ABC
```

Expected output: `1234ABC entered the parking lot`.

Read the saved file from a new container:

```bash
docker run --rm -v parking-lot-lab16-test:/app/data --entrypoint cat parking-lot:persistence /app/data/lot.json
```

The file should contain `1234ABC` and its entry time.

Register the car leaving, using another container:

```bash
docker run --rm -v parking-lot-lab16-test:/app/data parking-lot:persistence leave 1234ABC
```

Expected output: `1234ABC left the parking lot`.

Each command creates a new container. The `--rm` option removes that
container when it finishes, but the named volume keeps the parking state
available for the next run.
