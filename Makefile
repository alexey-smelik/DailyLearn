.PHONY: up down build restart logs ps \
        migrate migrate-create migrate-down \
        lint lint-api lint-core lint-tg lint-quiz \
        test test-api test-core test-tg test-quiz \
        ui-install ui-dev ui-build \
        ollama-pull-llama3 ollama-pull-phi3 ollama-list

# ── Docker Compose ─────────────────────────────────────────────────────────

up:
	docker compose up -d

up-build:
	docker compose up -d --build

down:
	docker compose down

down-volumes:
	docker compose down -v

build:
	docker compose build

restart:
	docker compose restart

logs:
	docker compose logs -f

logs-%:
	docker compose logs -f $*

ps:
	docker compose ps

# ── Database migrations (runs inside web-api venv) ─────────────────────────

migrate:
	$(MAKE) -C web-api migrate

migrate-create:
	$(MAKE) -C web-api migrate-create name="$(name)"

migrate-down:
	$(MAKE) -C web-api migrate-down

# ── Lint (all services) ────────────────────────────────────────────────────

lint: lint-api lint-core lint-tg lint-quiz

lint-api:
	$(MAKE) -C web-api lint

lint-core:
	$(MAKE) -C core lint

lint-tg:
	$(MAKE) -C tg-tool lint

lint-quiz:
	$(MAKE) -C quiz-service lint

# ── Tests (all services) ───────────────────────────────────────────────────

test: test-api test-core test-tg test-quiz

test-api:
	$(MAKE) -C web-api test

test-core:
	$(MAKE) -C core test

test-tg:
	$(MAKE) -C tg-tool test

test-quiz:
	$(MAKE) -C quiz-service test

# ── Frontend ───────────────────────────────────────────────────────────────

ui-install:
	npm --prefix web-ui ci

ui-dev:
	npm --prefix web-ui run dev

ui-build:
	npm --prefix web-ui run build

# ── Ollama model management ───────────────────────────────────────────────

ollama-pull-llama3:
	docker compose exec ollama ollama pull llama3

ollama-pull-phi3:
	docker compose exec ollama ollama pull phi3:mini

ollama-list:
	docker compose exec ollama ollama list
