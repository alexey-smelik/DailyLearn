# web-api

FastAPI backend for DailyLearn.

## Stack

- **FastAPI** — HTTP framework
- **SQLAlchemy 2.0** (async) + **asyncpg** — database ORM
- **PostgreSQL 16** — database
- **Alembic** — migrations
- **Pydantic v2** — request/response schemas
- **uv** — package manager

## Setup

```bash
uv sync
cp .env.example .env   # adjust DATABASE_URL if needed
```

## Commands

```bash
make install        # install dependencies
make run            # uvicorn on :8000 with --reload
make migrate        # alembic upgrade head
make migrate-create name="add_field"   # generate migration
make migrate-down   # downgrade one step
make lint           # ruff check + format check
make format         # ruff fix + format
make test           # pytest
make test-cov       # pytest with coverage (≥80%)

make docker-up      # docker compose up -d
make docker-down    # docker compose down
make docker-build   # rebuild web-api image
make docker-logs    # tail web-api logs
```

## API

Base prefix: `/api/v1`

| Method | Path | Description |
|--------|------|-------------|
| GET | `/users` | List all users |
| POST | `/users` | Create user |
| GET | `/users/{id}` | Get user |
| PATCH | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Delete user |
| GET | `/learning-cards` | List all cards |
| POST | `/learning-cards` | Create card |
| GET | `/learning-cards/{id}` | Get card |
| PATCH | `/learning-cards/{id}` | Update card |
| DELETE | `/learning-cards/{id}` | Delete card |
| GET | `/newsletters` | List all newsletters |
| POST | `/newsletters` | Create newsletter |
| GET | `/newsletters/{id}` | Get newsletter |
| PATCH | `/newsletters/{id}` | Update newsletter |
| DELETE | `/newsletters/{id}` | Delete newsletter |
| GET | `/health` | Health check |

Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Project structure

```
app/
  main.py              # FastAPI app, router registration
  database.py          # AsyncEngine, get_session dependency
  settings/config.py   # Pydantic BaseSettings
  models/              # SQLAlchemy ORM models
  repositories/        # DB access layer
  api/                 # Route handlers
  services/
    schemas.py         # Pydantic Create/Update/Response schemas
    exceptions.py      # Domain HTTP exceptions
alembic/               # Migrations
tests/                 # pytest + aiosqlite (SQLite in-memory)
```
