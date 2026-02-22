# web-ui

React frontend for DailyLearn.

## Stack

- **React 19** + **TypeScript** (strict) — UI
- **Vite 6** — dev server and bundler
- **TanStack Query v5** — server state management
- **CSS Modules** — scoped styles
- **Inter** font (Google Fonts)

## Setup

```bash
npm install
```

Requires `web-api` running on `:8000` (Vite proxy forwards `/api` → `http://localhost:8000`).

## Commands

```bash
npm run dev      # dev server on :5173
npm run build    # production build → dist/
npm run preview  # preview production build
npm run lint     # ESLint
```

## Features

- **Login** — enter any login; user is fetched or created automatically
- **Card grid** — shows all learning cards for the logged-in user
- **Add card** — modal form with name, source URL, and schedule
- **Edit / delete card** — click any card to open the edit modal

## Project structure

```
src/
  main.tsx
  App.tsx
  index.css                  # CSS variables, reset, Inter font
  shared/
    api/client.ts            # fetch wrapper (get/post/patch/delete)
    components/Modal.tsx     # backdrop modal with animation
  features/
    auth/
      types.ts
      api.ts                 # getOrCreateUser(login)
      hooks/useAuth.ts       # localStorage session persistence
      components/LoginModal.tsx
    cards/
      types.ts
      api.ts                 # getCards, createCard, updateCard, deleteCard
      hooks/useCards.ts      # TanStack Query hooks
      components/
        CardGrid.tsx         # main page layout
        CardItem.tsx         # individual card tile
        CardForm.tsx         # create / edit modal form
```

## API

Proxied via Vite to `http://localhost:8000/api/v1`:

| Method | Path | Usage |
|--------|------|-------|
| GET | `/users` | Find user by login |
| POST | `/users` | Create user on first login |
| GET | `/learning-cards` | Load cards (filtered by `user_id`) |
| POST | `/learning-cards` | Create card |
| PATCH | `/learning-cards/{id}` | Update card |
| DELETE | `/learning-cards/{id}` | Delete card |
