# FastAPI Event Service

A minimal yet production‑ready FastAPI backend service for receiving, storing, and querying events via HTTP APIs.

This project is designed as a lightweight **event / signal ingestion service** and a reusable backend template with clear separation between **development, testing, and production** environments.

---

## Features

- RESTful API for event ingestion and querying
- SQLite backend with SQLAlchemy ORM
- Explicit environment separation: `dev` / `test` / `prod`
- Fully tested with `pytest` (≈96% coverage)
- Dockerized for local and server deployment
- Persistent storage via Docker volume in production mode

---

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite
- pytest + pytest-cov
- Docker

---

## API Endpoints

| Method | Path      | Description            |
|------|-----------|------------------------|
| POST | `/events` | Create a new event     |
| GET  | `/events` | List stored events     |
| GET  | `/health` | Health check endpoint  |

---

## Local Development

### 1. Setup virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run the service

```bash
uvicorn app.main:app --reload
```

Service will be available at:

```
http://127.0.0.1:8000
```

---

## Running Tests

All tests run against an **in‑memory SQLite database**.

```bash
pytest
```

Run tests with coverage report:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## Docker Deployment (v0.1.0)

### Build image

```bash
docker build -t fastapi-event-service:v1 .
```

### Run container (ephemeral data)

```bash
docker run --rm \
  -p 8000:8000 \
  -e APP_ENV=prod \
  fastapi-event-service:v1
```

### Run container with persistent volume

```bash
docker run --rm \
  -p 8000:8000 \
  -e APP_ENV=prod \
  -v $(pwd)/data:/app/data \
  fastapi-event-service:v1
```

Database will be stored at:

```
data/prod.db
```

---

## Environment Configuration

| Environment | APP_ENV | Database            |
|------------|---------|---------------------|
| Development | dev     | `data/dev.db`       |
| Testing     | test    | In‑memory SQLite    |
| Production  | prod    | `data/prod.db`      |

Optional environment variables:

- `API_TOKEN`: enable simple API token authentication (optional)

---

## Project Scope

- Backend API service only
- No frontend included
- Intended as a reusable internal service template

---

## Versioning

- `v0.1.0`: Local development, testing, and Docker deployment fully validated

---

## License

MIT

<!-- PR flow verification -->
