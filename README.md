# URL shortener prototype

A Python backend learning project with FastAPI, Redis and asynchronous SQLAlchemy.

## Current scope

The source implements URL validation, deterministic SHA-256/Base62 identifiers, a create-link endpoint, a redirect endpoint and Redis caching.
Redis cache entries expire; durable database links do not have implemented expiration.
Custom aliases, hit statistics and Docker deployment are not implemented in this tree.

## Repository layout

- `app.py`: FastAPI routes.
- `functions.py`: identifier generation and cache/database coordination.
- `Pydantic_dir/`: request and settings models.
- `Redis/`: cache integration.
- `test_db/`: database modules and a committed SQLite file.
- `frontend/`: static browser UI.
- `tests/`: API, function, database and cache test drafts.
- `.github/workflows/hello_test.yml`: existing test workflow.

## Installation and current blocker

Create and activate a Python virtual environment, then install the actual dependency file:

```sh
python -m pip install -r requirements
```

**The default branch is currently not runnable as a clean checkout:** imports refer to a `DB` package, but the database directory is named `test_db`.
Resolve these imports consistently before using the intended command:

```sh
python -m uvicorn app:app --host localhost --port 8003
```

Redis is expected on localhost:6379. The frontend and generated short URLs use localhost:8003.
PostgreSQL initialization is incomplete; setting `POSTG` does not create an engine.

## Settings actually read

`Pydantic_dir/pydantic_valid_classes.py` reads these from the environment or a local `.env`:

- `EXP_TIME`: Redis TTL in seconds (default 3600).
- `TEST_MODE`: changes redirect output (default false).
- `SHORT_ID_LENGTH`: requested identifier truncation length (default 7).

The implementation hashes only 32 bits before Base62 encoding; this does not guarantee seven characters or unique identifiers.

## Tests and known issues

The existing workflow runs `pytest -v tests/` with Redis and extra test dependencies.
The latest reviewed default-branch run failed; this documentation change does not repair CI.

Tests currently disagree with async function signatures, generated URL schemes, validation status codes and TEST_MODE redirect behavior.
Database tests delete records through the configured session; do not point them at valuable data.
Persistence errors are swallowed by the insert function and cache writes can proceed without durable storage.
Committed database records have not been certified as safe fixtures.

No Dockerfile, configurable public domain, custom aliases or hit statistics are claimed here.
