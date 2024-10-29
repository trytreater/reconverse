# Reconverse

Recall relevant information from previous conversations.

## Development setup

Install [`uv`](https://github.com/astral-sh/uv) if it's not already installed:

```
pip install uv
```

Sync the project:

```
uv sync
```

Copy `env.example` to `.env` and fill in the values.

You'll want to start the necessary databases for local development using docker.

```
docker compose up -d
```

Tests can be run via `pytest` through `uv`:

```
uv run pytest
```

Linting and formatting is done via `ruff`:

```
uv run ruff check
uv run ruff format
```

We use [Mint](https://rwx.com/mint) for CI. Tests and formatting/linting are run in CI as well; the definition is at [.mint/ci.yml](./.mint/ci.yml).
