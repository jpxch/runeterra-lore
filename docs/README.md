# Runeterra Lore

Runeterra Lore is Riot's official lore explorer: a unified application for champions, skins, regions, and alternate universes (AUs).
The purpose is to provide a single, canonical source of truth for both Rioters and players.

---

## 🚀 Getting Started

### Requirements
- Python 3.10+
- Node.js 20+
- PNPM
- Docker & Docker Compose
- Poetry

### Setup
```bash
git clone https://git.riotgames.com/runeterra-lore.git
cd runeterra-lore
make dev
```
This launches backend (FastAPI), frontend (React + Vite), and seeds data.

### Run Tests
```bash
make test
```

### Build Production
```bash
make build
```

---

## 📂 Structure
- `backend/` → FastAPI services
- `frontend/` → React client
- `data/` → canonical champion/skin/region JSON
- `docs/` → project documentation

---

## 📜 Canon
- Data is authoritative from Riot Narrative team.
- Retcons are respected.
- All lore content must pass **Narrative Review** before merging.
