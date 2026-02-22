# DailyLearn

Spaced repetition learning app based on the Ebbinghaus Forgetting Curve.

## Services

| Service | Stack | Port |
|---------|-------|------|
| `web-api` | FastAPI + SQLAlchemy 2.0 + PostgreSQL | 8000 |
| `web-ui`  | React 19 + TypeScript + Vite | 5173 |
| `tg-tool` | FastAPI + aiogram 3.x | 8001 |
| `core`    | APScheduler + asyncpg | — |

## Quick start

```bash
# Start PostgreSQL
docker compose up -d postgres

# Backend
cd web-api && make install && make migrate && make run

# Frontend (separate terminal)
cd web-ui && npm install && npm run dev
```

Open [http://localhost:5173](http://localhost:5173), enter a login and start adding learning cards.

## Architecture

Review intervals: **1d → 3d → 7d → 14d → 30d → 90d**

```
next_review = last_review + interval_days * difficulty_factor
```

## Feature plan

- [ ] Github CI/CD
- [ ] Card notes — rich-text description field per card
- [ ] Statistics dashboard — review streaks, cards due today, retention rate chart
- [ ] Schedule presets — one-click templates (e.g. "Aggressive 1d→3d→7d", "Relaxed 7d→21d→60d")
- [ ] Redesign Web UI / UX
- [ ] Prepare smart-plan learning with auto pushes
- [ ] Smart feedback aggregation
- [ ] Local demon supporting
- [ ] Obsidian integration for local demon
- [ ] Telegram support editing cards / feedback
- [ ] Update test-coverage
- [ ] CSV / JSON import & export
- [ ] Tags — free-form labels in addition to groups
- [ ] PWA support — offline access and browser push notifications
- [ ] Card priority — pin urgent cards to the top of the queue
- [ ] Telegram group notifications — send reminders to a shared group chat for team learning

## License

MIT
