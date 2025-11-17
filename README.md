# carobama

A real-time Emporer Servers live timing data analysis tool.

This repository contains a small utility to connect to Emporer Servers' live race-control websocket and parse connected driver information for downstream timing/analysis workflows.

## Features

- Connects to the Emporer Servers race-control websocket endpoint and listens for live events
- Parses connected drivers and builds a small in-memory list of team drivers and driver names
- Minimal, easy-to-extend codebase for live timing and telemetry experiments

## Quick start (for developers)

Prerequisites

- Python 3.8 or newer
- Git

Recommended: create and use a virtual environment for development.

Install dependencies

```bash
# create and activate a venv (zsh)
python3 -m venv .venv
source .venv/bin/activate

# install required packages
pip install -r requirements.txt
```

Run the websocket reader

```bash
python websocket_reader.py
```

When run, the script will open a websocket connection to the default endpoint defined in `websocket_reader.py` and print some parsed driver information to stdout.

## Files of interest

- `websocket_reader.py` – main small example that opens the websocket, parses messages and collects connected driver info.
- `requirements.txt` – lists runtime dependencies (currently `websocket-client`).

## Development notes

- The websocket URL is currently hard-coded in `websocket_reader.py` (the default is `wss://yorkfs.emperorservers.com/api/race-control`). If you need to point to a different server or a local test harness, edit the URL in the `WebsocketReader` constructor or extend the script to accept a command-line argument or environment variable.
- The current implementation prints driver info; for production use you may want to:
	- add structured logging
	- persist events to a database or message queue
	- add robust reconnect/backoff logic and error handling
	- add unit tests around parsing logic

## Contributing

Contributions are welcome. Please open an issue first describing the change you want to make, or open a pull request with a short description and tests where applicable.

## Troubleshooting

- If you see SSL/wss errors, ensure your environment allows outgoing TLS websocket connections and that Python's cert store is up-to-date.
- If you don't receive messages, verify the endpoint and any authentication requirements with the Emporer Servers team.

## License & contact

Add your preferred license and contact information here.
