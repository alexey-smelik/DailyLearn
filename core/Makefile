.PHONY: install run lint format test test-cov

install:
	uv sync

run:
	uv run python -m app.main

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

test:
	uv run pytest

test-cov:
	uv run pytest --cov=app --cov-fail-under=80
