.PHONY: install run lint format test test-cov \
        docker-build docker-up docker-down docker-logs \
        ollama-pull-llama3 ollama-pull-phi3

# ── Local dev ──────────────────────────────────────────────────────────────────

install:
	uv sync

run:
	uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8002

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

# ── Docker (via root compose) ─────────────────────────────────────────────────

docker-build:
	docker compose -f ../docker-compose.yaml build quiz-service

docker-up:
	docker compose -f ../docker-compose.yaml up -d quiz-service ollama

docker-down:
	docker compose -f ../docker-compose.yaml down

docker-logs:
	docker compose -f ../docker-compose.yaml logs -f quiz-service

# ── Ollama model management ───────────────────────────────────────────────────

ollama-pull-llama3:
	docker compose -f ../docker-compose.yaml exec ollama ollama pull llama3

ollama-pull-phi3:
	docker compose -f ../docker-compose.yaml exec ollama ollama pull phi3:mini

ollama-list:
	docker compose -f ../docker-compose.yaml exec ollama ollama list
