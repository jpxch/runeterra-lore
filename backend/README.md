# Runeterra Backend

FastAPI service for Runeterra Lore API
# Full-Spectrum Labs — Runeterra Division

FSL Runeterra is a research-grade data and simulation service exploring the narrative systems of League of Legends.  
It is not affiliated with Riot Games; it is an independent Full-Spectrum Labs experiment built for educational, analytical, and creative study.

---

## ✨ Mission

“Knowledge belongs to those who reach for it.”

Full-Spectrum Labs engineers world-class, open systems that let developers, storytellers, and researchers dissect and reimagine digital universes.

---

## 🧠 Stack Overview
| Layer | Tech |
|-------|------|
| **Backend** | FastAPI + Pydantic v2 + Poetry |
| **Frontend** | Next.js 15 (TypeScript + SCSS) |
| **Data** | Canonical JSON caches (champions, skins, regions) generated from DDragon |
| **Infra** | Docker Compose + Makefile tooling |
| **Style** | FSL Engineering Standard |

---

## ⚡ Quick Start

```bash
poetry install
poetry run uvicorn backend.main:app --reload
# visit http://127.0.0.1:8000/api/champions
🧭 Structure
backend/     →  FastAPI service
frontend/    →  Next.js interface
data/        →  Canonical caches
docs/        →  Internal FSL documents
infra/       →  Docker + CI/CD
shared/      →  Codegen & Schemas
🪞 Attribution
All Riot Games universe data © Riot Games, Inc. Used under Fan Content Policy.
Full-Spectrum Labs is a private research studio building educational tools and frameworks.