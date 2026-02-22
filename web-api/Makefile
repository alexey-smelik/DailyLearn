.PHONY: install run migrate migrate-create migrate-down lint format test test-cov \
        docker-build docker-up docker-down docker-logs

install:
	uv sync

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	uv run alembic upgrade head

migrate-create:
	uv run alembic revision --autogenerate -m "$(name)"

migrate-down:
	uv run alembic downgrade -1

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff format .
	uv run ruff check --fix .

test:
	uv run pytest -v

test-cov:
	uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=80

docker-build:
	docker compose -f ../docker-compose.yaml build web-api

docker-up:
	docker compose -f ../docker-compose.yaml up -d

docker-down:
	docker compose -f ../docker-compose.yaml down

docker-logs:
	docker compose -f ../docker-compose.yaml logs -f web-api
