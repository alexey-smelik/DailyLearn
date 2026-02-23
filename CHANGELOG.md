# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.3] — 2026-02-23

### Added
- **Copy button on cards** — hovering a card reveals a `⎘` icon button in the top-right corner.
  Clicking it copies the card name (and source URL on a new line, if set) to the clipboard.
  The button briefly shows `✓` in green for 2 seconds to confirm the action.

---

## [1.0.2] — 2026-02-23

### Added
- **Ebbinghaus Schedule Builder** (`ScheduleBuilder` component) — replaces the raw text input
  for the review schedule field in the card form:
  - Three built-in presets: **Ebbinghaus** (1d → 3d → 7d → 14d → 30d → 90d),
    **Fast** (1d → 2d → 5d → 14d → 30d), **Deep** (7d → 14d → 30d → 60d → 180d).
  - **Custom** mode: click any interval chip to edit it inline, add new chips, or remove existing ones.
    Supported units: `m` (minutes), `h` (hours), `d` (days).
  - **Cumulative timeline** — shows actual review dates from card creation
    (e.g. Day 1 · Day 4 · Day 11 · Day 25 · Day 55 · Day 145).
  - Produces the same `"1d → 3d → 7d"` string format — no backend changes required.
- **Study timer quick-picks** — the study timer field now shows preset duration buttons
  (30 min, 1 h, 2 h, 1 day, 3 days, 1 week) alongside a free-text custom input.

---

## [1.0.1] — 2026-02-23

### Added
- **Topics section in the sidebar** — group/topic navigation moved from the horizontal filter
  bar inside the card grid into the left sidebar:
  - "All Cards" entry always shown at the top of the Topics section.
  - Each user group listed as a nav item with a hover-reveal delete button.
  - Inline "+ New Topic" creation: type a name, confirm with Enter or the `+` button,
    cancel with Escape.
  - Active topic highlighted with the accent colour; selecting a topic filters the card grid.

### Changed
- `selectedGroup` state and `useGroups` hook lifted from `CardGrid` up to a new
  `AuthenticatedApp` inner component in `App.tsx`, so both `Sidebar` and `CardGrid`
  share the same selection.
- Horizontal group filter bar and all related CSS removed from `CardGrid`.
- "Group" label renamed to "Topic" across the card form and sidebar for consistency.

---

## [1.0.0] — 2026-02-23

### Added
- Initial release of **DailyLearn** — spaced-repetition learning app based on the
  Ebbinghaus Forgetting Curve.
- **Core service** — APScheduler-based job that checks due learning cards every minute
  and dispatches Telegram notifications using the `1d → 3d → 7d → 14d → 30d → 90d`
  default interval chain.
- **Web API** (`web-api`) — FastAPI + SQLAlchemy 2.0 async, PostgreSQL, Alembic migrations.
  Endpoints for learning cards, card groups, users, newsletters, skip, toggle, and
  test-send.
- **Telegram bot** (`tg-tool`) — aiogram 3.x webhook bot. Inline keyboard buttons:
  Pause, Skip, and optional Quiz. Handles conspect (study notes) collection via
  conversation states.
- **Quiz service** (`quiz-service`) — FastAPI service that generates quizzes from card
  conspects using a local Ollama LLM (default: `phi3:mini`). Supports multiple-choice
  and open-ended question types, configurable difficulty, tenacity retry logic, and
  JSON schema validation with lenient item-level recovery.
- **Web UI** (`web-ui`) — React 19 + TypeScript SPA. Card grid, card form with all
  settings, login modal, sidebar navigation.
- Docker Compose orchestration for all services including PostgreSQL and Ollama.
