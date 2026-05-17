# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CareLink is a full-stack web application for searching and comparing aged care facilities in Australia. The stack is: **Vue 3 + Vite** (frontend) + **FastAPI + PostgreSQL** (backend) + Python-based ML/data processing.

## Commands

### Backend
```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload          # dev server on :8000
pytest tests/                          # run tests
```

### Frontend
```bash
cd frontend
npm install
npm run dev        # dev server on :5173
npm run build      # production build → dist/
npm run preview    # preview production build
```

## Architecture

### Backend (`backend/app/`)
Layered FastAPI app with strict separation:

- `routers/` — thin HTTP handlers, delegate to services, apply rate limiting
- `services/` — all business logic (queries, ML predictions, wait time calc)
- `models/` — SQLAlchemy async ORM models
- `schemas/` — Pydantic v2 request/response models
- `core/config.py` — Pydantic `Settings` loaded from `.env`
- `core/database.py` — async engine + `AsyncSession` factory

All DB access is **async** (asyncpg driver, `AsyncSession`). Business logic lives in services; routers must not contain queries.

Key models:
- `AgedCareService` — main facility table (address, capacity, funding)
- `FacilityAvailabilityML` — ML-predicted availability (K-means output)
- `StarRating` — quality ratings
- `Location` — geocoded coordinates

### Frontend (`frontend/src/`)
Vue 3 Composition API throughout:

- `views/` — page components (one per route)
- `components/` — reusable UI components
- `stores/` — Pinia stores: `locationStore` (search state), `compareStore` (comparison cart)
- `services/facilitiesApi.js` — single API client (fetch wrapper); all backend calls go through here
- `composables/` — shared Composition API logic (e.g., scroll animations)
- `router/index.js` — includes auth guard (checks localStorage) and scroll behavior

Simple password-based auth gate via `PasswordPage.vue` + localStorage; no JWT.

### ML Availability (`ai+ml/`)
K-means clustering on 3 features: facility supply, regional demand/supply ratio, facility supply share. Produces labels: "Likely Available", "Possibly Available", "Likely Unavailable". Predictions are stored in `FacilityAvailabilityML` and served by `facility_service.py`.

### API Routes (`/api/v1/`)
| Route | Purpose |
|---|---|
| `GET /facilities/search` | Filtered search (suburb, postcode, care_type, beds, remoteness, distance) |
| `GET /facilities/{id}` | Facility detail |
| `GET /facilities/{id}/similar` | Similar facilities |
| `GET /facilities/map` | Map markers |
| `GET /facilities/recommended` | Location-based recommendations |
| `GET /search/autocomplete` | Suburb/facility name autocomplete |
| `POST /waittime/estimate` | Wait time estimation |
| `GET /health` | Health check |

## Environment Variables

**Backend** (`.env` in `backend/`):
```
DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_SSLMODE=require
```

**Frontend** (`.env` in `frontend/`):
```
VITE_API_BASE_URL=http://localhost:8000
```

## Key Conventions

- **CORS**: allowed origins are hardcoded in `app/main.py` — add new origins there when deploying to new domains.
- **Rate limiting**: slowapi, IP-based; defaults 30 req/min. Applied as decorator on router functions.
- **Caching**: `fastapi-cache2` with `InMemoryBackend`; map endpoints cached 300 s, detail/similar 600 s.
- **Distance**: Haversine formula used for proximity searches — coordinate math is in `facility_service.py`.
- **Pagination**: all list endpoints use `limit`/`offset` query params.
- **Input validation**: postcode and text inputs validated with regex in router layer before reaching services.
- **Deployment**: frontend on Vercel (`vercel.json` present); backend on Uvicorn behind a reverse proxy.
