# bookmarks

FastAPI + HTMX + Plain CSS. No frameworks, no build step, no bloat.

## Usage

```bash
./start.sh   # Start (downloads HTMX, finds free port)
./stop.sh    # Stop
./status.sh  # Check status
```

## Endpoints

- `GET /` — Home
- `GET /health` — Health check

## Stack

- **FastAPI** — Python backend
- **HTMX** — Interactivity via hypermedia
- **Plain CSS** — No Tailwind runtime, no preprocessor

## PID Tracking

Services register in `../services.pid` for centralized management.
