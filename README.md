# Parking-lot

Parking-lot is a command-line tool for parking lot staff. From the terminal they can
register cars entering and leaving, check whether a car is inside, see how many spaces
are free and calculate how much a driver has to pay, with a daily price cap.
The parking state is saved in a JSON file, so it is kept between commands.

## Requirements

- [Git](https://git-scm.com/downloads)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (it installs Python 3.13 for you)
- [Docker](https://docs.docker.com/get-docker/), only for the "Run with Docker" section

## Install

```
git clone https://github.com/esade-swdev-2026/parking-lot.git
cd parking-lot
uv sync
```

`uv sync` creates a virtual environment and installs the exact versions pinned in
`uv.lock`, including the development tools. Run every command below from the
`parking-lot` folder.

## Run

### A day in the parking lot

These commands share the saved parking state in `data/lot.json`. The file and the
`data/` folder are created by the first `enter`; `data/` is ignored by Git.

```
uv run parking-lot enter 1234ABC
uv run parking-lot enter 5678DEF
uv run parking-lot check-if-car-inside 1234ABC
uv run parking-lot free
uv run parking-lot full
uv run parking-lot leave 1234ABC
uv run parking-lot leave 5678DEF
```

Expected output:

```
1234ABC entered the parking lot
5678DEF entered the parking lot
1234ABC is inside the parking lot
98 free spaces
There are free spaces
1234ABC left the parking lot
Parked for 0 minutes
Price to pay with daily cap: 0.00€
5678DEF left the parking lot
Parked for 0 minutes
Price to pay with daily cap: 0.00€
```

`leave` charges the time between `enter` and `leave` (0 minutes here, because the car
has just entered), at 0.05€ per minute with a cap of 20€ for each 24 hours.
Change them with `--price-per-minute` and `--daily-cap`.

The lot has 100 spaces by default. The capacity is not saved, so pass the same
`--capacity` to `enter`, `free` and `full` if you use another one.
Use `--lot-file` to keep the state in a different file.

### Quick calculations

These commands do not read or change the saved state:

```
uv run parking-lot free 30
uv run parking-lot free 30 --capacity 50
uv run parking-lot full 100
uv run parking-lot price 60
uv run parking-lot price 60 --price-per-minute 0.10
uv run parking-lot price-with-cap 2000
uv run parking-lot stay 9 40 11 15
uv run parking-lot check-if-car-inside 1234ABC --parked "1234ABC,5678DEF"
```

Expected output:

```
70 free spaces
20 free spaces
The parking is full
Price to pay for the parking: 3.00€
Price to pay for the parking: 6.00€
Price to pay with daily cap: 40.00€
Parked for 95 minutes
Price to pay for the parking: 4.75€
1234ABC is inside the parking lot
```

`free` and `full` read the saved lot when you do not give the number of occupied
spaces. `check-if-car-inside` reads the saved lot unless you give a list of plates
with `--parked`; then it only looks in that list.

### Commands

| Command | What it does | Options |
|---|---|---|
| `enter PLATE` | Saves a car and its entry time | `--capacity`, `--lot-file` |
| `leave PLATE` | Removes a car and shows the minutes and the price | `--price-per-minute`, `--daily-cap`, `--lot-file` |
| `check-if-car-inside PLATE` | Says whether a car is inside | `--parked`, `--lot-file` |
| `free [OCCUPIED]` | Free spaces | `--capacity`, `--lot-file` |
| `full [OCCUPIED]` | Whether the lot is full | `--capacity`, `--lot-file` |
| `price MINUTES` | Price for some minutes | `--price-per-minute` |
| `price-with-cap MINUTES` | Price with a cap per 24 hours | `--price-per-minute`, `--daily-cap` |
| `stay H M H M` | Minutes and price between two times of the same day | `--price-per-minute` |

Run `uv run parking-lot COMMAND --help` for the details of each command.

### Errors

Bad input gives a clear message and exit code 1 (or 2 for a wrong argument type),
never a traceback. For example:

```
uv run parking-lot enter 1234ABC
uv run parking-lot enter 1234ABC
uv run parking-lot leave 9999ZZZ
uv run parking-lot enter '!!@@'
uv run parking-lot leave 1234ABC
```

Expected output:

```
1234ABC entered the parking lot
1234ABC is already inside
9999ZZZ is not inside
!!@@ is not a valid license plate: use 2 to 10 letters or digits
1234ABC left the parking lot
Parked for 0 minutes
Price to pay with daily cap: 0.00€
```

A plate has 2 to 10 letters or digits; lowercase is turned into uppercase. If
`data/lot.json` is damaged, every command says so and stops without overwriting it.

## Develop

```
uv run ruff check .          # lint
uv run ruff format .         # format (CI runs `--check` and fails on a diff)
uv run mypy src tests        # types (strict)
uv run pytest                # tests
```

These four commands are exactly what `.github/workflows/check.yml` runs on every push.
If they pass here, CI passes. When you change a dependency in `pyproject.toml`, run
`uv lock` and commit the updated `uv.lock`; CI fails if the two disagree.

## Layout

```
src/parking_lot/
  cli.py                 the Typer commands: read input, call the functions, print
  parking_functions.py   pure functions: plates, spaces, entering, leaving, minutes, price
  pricing.py             pure function: price with a daily cap
  storage.py             reads and writes data/lot.json
  __main__.py            lets `python -m parking_lot` work
tests/                   pytest tests, one file per module
Dockerfile               the image the release pipeline publishes
.github/workflows/       check.yml (every push) and release.yml (v1.0 tag)
pyproject.toml           dependencies and tool configuration
```

The computation lives in pure functions that take and return plain data, and they
raise `ValueError` for invalid input. `cli.py` is a thin layer that catches those
errors, prints the message and exits with code 1.

## Use of AI

We used AI assistants as support tools during the project:

- **ChatGPT**, during the first sessions, to understand Git and Docker commands,
  troubleshoot merge conflicts and get feedback on our code, tests and documentation.
- **Claude** (Anthropic), for the final submission, to review the project against the
  rubric and find bugs and edge cases (for example, `check-if-car-inside` ignoring the
  saved lot, and tracebacks with a damaged `lot.json`). It proposed code and tests for
  those fixes, the `leave` price, the Docker release test and this README.

Every change went through a pull request reviewed by another member of the group. We ran
the tests, the type checker and every README command ourselves before merging. The
final decisions and the responsibility for the code are ours.

## Run with Docker

Start Docker and run these commands from the `parking-lot` folder.

### Build the image

```
docker build -t parking-lot .
docker run --rm parking-lot --help
```

### Data that survives `docker rm`

The app saves its state in `/app/data/lot.json` inside the container. A named volume
keeps that folder outside the image. Each `docker run --rm` creates a new container
and removes it when it finishes, but the volume keeps the parking state for the next one.

```
docker volume rm --force parking-lot-data
docker run --rm -v parking-lot-data:/app/data parking-lot enter 1234ABC
docker run --rm -v parking-lot-data:/app/data parking-lot check-if-car-inside 1234ABC
docker run --rm -v parking-lot-data:/app/data --entrypoint cat parking-lot /app/data/lot.json
docker run --rm -v parking-lot-data:/app/data parking-lot leave 1234ABC
```

The first command starts from an empty lot, so you can repeat the whole block.
Expected output: `1234ABC entered the parking lot`, then `1234ABC is inside the parking lot`,
then the JSON file with `1234ABC` and its entry time, and finally the `leave` message
with the minutes and the price.

### Use the published image

The release pipeline publishes the image to GitHub Container Registry when the `v1.0`
tag is pushed. To run it without building anything:

```
docker pull ghcr.io/esade-swdev-2026/parking-lot:v1.0
docker volume rm --force parking-lot-data
docker run --rm -v parking-lot-data:/app/data ghcr.io/esade-swdev-2026/parking-lot:v1.0 enter 1234ABC
docker run --rm -v parking-lot-data:/app/data ghcr.io/esade-swdev-2026/parking-lot:v1.0 check-if-car-inside 1234ABC
docker run --rm -v parking-lot-data:/app/data ghcr.io/esade-swdev-2026/parking-lot:v1.0 leave 1234ABC
```
