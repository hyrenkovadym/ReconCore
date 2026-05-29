# ReconCore

ReconCore is a backend-heavy reconciliation and data quality platform.

This repository is being built in stages.  
Current stage: **Step 1 - Project structure and Docker Compose setup**.

## Stack (Target)

- Backend: FastAPI, SQLAlchemy, Alembic, Celery
- Data stores: PostgreSQL, MongoDB, Redis
- Queue: RabbitMQ
- Frontend: Next.js + TypeScript + Tailwind CSS
- Storage and integrations: AWS S3, external connectors, webhooks

## Current Structure

```text
.
├── backend
│   ├── app
│   │   ├── api
│   │   │   └── v1
│   │   │       ├── endpoints
│   │   │       └── router.py
│   │   ├── core
│   │   │   └── config.py
│   │   ├── db
│   │   ├── modules
│   │   │   ├── auth
│   │   │   ├── connectors
│   │   │   ├── ingestion
│   │   │   ├── jobs
│   │   │   ├── monitoring
│   │   │   └── reconciliation
│   │   ├── workers
│   │   │   ├── celery_app.py
│   │   │   └── tasks.py
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
├── frontend
│   ├── app
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.mjs
│   └── tsconfig.json
├── docker-compose.yml
└── .env.example
```

## Services in Docker Compose

- `postgres`: normalized business data
- `mongo`: raw payload storage
- `redis`: cache, lock, temporary state, Celery result backend
- `rabbitmq`: Celery broker
- `backend`: FastAPI API server
- `worker`: Celery worker
- `beat`: Celery scheduler
- `frontend`: Next.js dashboard shell

## Local Run (Current Stage)

1. Create env file:

```bash
cp .env.example .env
```

2. Build and run:

```bash
docker compose up --build
```

3. Open:

- API root: `http://localhost:8000/`
- API docs: `http://localhost:8000/docs`
- API health: `http://localhost:8000/api/v1/health/`
- Dashboard: `http://localhost:3000/`
- RabbitMQ UI: `http://localhost:15672/`

## What Comes Next

Step 2 will add:

- SQLAlchemy models and database session management
- Alembic migration setup
- MongoDB and Redis client modules
- shared repository/service foundations

