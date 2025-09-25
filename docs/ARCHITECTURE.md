# Architecture Overview

## System Diagram (high-level)
Frontend (React + Vite) → Backend API (FastAPI) → Data Layer (Canonical JSON / DB)

## Components
### Frontend
- React + Vite + Tailwind.
- Champion search, region browser, AU timelines.
- i18n-ready with language switcher.

### Backend
- FastAPI microservice with Swagger/OpenAPI spec.
- Endpoints: `/champions`, `/regions`, `/skins`, `/aus`.
- Pydantic models for strict schemas.

### Data Layer
- JSON seeds + Riot's internal narrative DB.
- Planned: Postgres for scalable queries & timelines.

### Infra
- Docker Compose for dev parity.
- Kubernetes + Helm for staging/prod.
- Observability via logs + metrics + traces.