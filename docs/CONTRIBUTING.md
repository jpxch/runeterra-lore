# Contributing Guidelines (Riot Coding Standards)

## 1. Philosophy

- **Production quality from day one** — no quick hacks or throwaway code.
- **Consistency > Cleverness** — every file follows the same structure.
- **Defensive by default** — APIs return clear errors, never raw tracebacks.
- **Contracts first** — models define data shape before code consumes it.
- **Backend + Frontend in parallel** — both evolve together against the same contract.

---

## 2. Backend Standards

### Imports

- Standard library → third-party → internal modules.

### Data Loading

- Always use `services/loader.py`.
- Empty or missing JSON must resolve to `[]` or `{}`, never crash.

### Models

- Defined in `backend/models/` with `pydantic.BaseModel`.
- Use strict typing (`Optional`, `List`, `Dict`).
- Provide separate `Summary` vs `Detail` models.

### API Routes

- Each domain (`champions`, `regions`, `skins`, `relationships`) lives in `backend/api/`.
- Always include `response_model` for Swagger docs.
- Explicit error handling:
  - `404` → item missing
  - `500` → bad data link

### Docstrings

- Every route + model has a docstring describing purpose.

### Tests

- Use `pytest` in `backend/tests/`.
- Each endpoint needs at least:
  - ✅ success test
  - ✅ error test

---

## 3. Frontend Standards

### Imports

- Type-only imports use `import type`.
- Group React/third-party imports before local.

### Components

- One concern per component:
  - `ChampionAbilities.tsx`
  - `ChampionSkins.tsx`
  - `ChampionRelationships.tsx`
- Props must be typed.

### API Layer

- `src/lib/api.ts` mirrors backend Pydantic models.
- Contracts updated here **before** pages/components.

### Pages

- Orchestrate components + fetch data.
- Keep them thin, no giant mixed files.

### Error + Loading States

- Always explicit — never leave blank screens.

---

## 4. Repo Structure

❯ tree
.
├── backend
│ ├── api
│ │ ├── champions.py
│ │ ├── **init**.py
│ │ ├── **pycache**
│ │ │ ├── champions.cpython-310.pyc
│ │ │ ├── **init**.cpython-310.pyc
│ │ │ ├── regions.cpython-310.pyc
│ │ │ └── skins.cpython-310.pyc
│ │ ├── regions.py
│ │ └── skins.py
│ ├── db
│ │ └── **init**.py
│ ├── main.py
│ ├── models
│ │ ├── champion.py
│ │ ├── **pycache**
│ │ │ ├── champion.cpython-310.pyc
│ │ │ ├── region.cpython-310.pyc
│ │ │ └── skin.cpython-310.pyc
│ │ ├── region.py
│ │ └── skin.py
│ ├── poetry.lock
│ ├── **pycache**
│ │ └── main.cpython-310.pyc
│ ├── pyproject.toml
│ └── services
│ ├── **init**.py
│ ├── loader.py
│ └── **pycache**
│ ├── **init**.cpython-310.pyc
│ └── loader.cpython-310.pyc
├── data
│ ├── champions.json
│ ├── regions.json
│ ├── relationships.json
│ └── skins.json
├── docs
│ ├── CONTRIBUTING.md
│ ├── LORE*GUIDE.md
│ └── ROADMAP.md
├── frontend
│ ├── eslint.config.js
│ ├── index.html
│ ├── node_modules
│ │ ├── d3 -> .pnpm/d3@7.9.0/node_modules/d3
│ │ ├── @eslint
│ │ │ └── js -> ../.pnpm/@eslint+js@9.36.0/node_modules/@eslint/js
│ │ ├── eslint -> .pnpm/eslint@9.36.0/node_modules/eslint
│ │ ├── eslint-plugin-react-hooks -> .pnpm/eslint-plugin-react-hooks@5.2.0_eslint@9.36.0/node_modules/eslint-plugin-react-hooks
│ │ ├── eslint-plugin-react-refresh -> .pnpm/eslint-plugin-react-refresh@0.4.20_eslint@9.36.0/node_modules/eslint-plugin-react-refresh
│ │ ├── globals -> .pnpm/globals@16.4.0/node_modules/globals
│ │ ├── react -> .pnpm/react@19.1.1/node_modules/react
│ │ ├── react-dom -> .pnpm/react-dom@19.1.1_react@19.1.1/node_modules/react-dom
│ │ ├── react-router-dom -> .pnpm/react-router-dom@7.9.1_react-dom@19.1.1_react@19.1.1__react@19.1.1/node_modules/react-router-dom
│ │ ├── recharts -> .pnpm/recharts@3.2.1*@types+react@19.1.13_react-dom@19.1.1_react@19.1.1__react-is@19.1.1_react@19.1.1_redux@5.0.1/node*modules/recharts
│ │ ├── @types
│ │ │ ├── react -> ../.pnpm/@types+react@19.1.13/node_modules/@types/react
│ │ │ └── react-dom -> ../.pnpm/@types+react-dom@19.1.9*@types+react@19.1.13/node_modules/@types/react-dom
│ │ ├── typescript -> .pnpm/typescript@5.8.3/node_modules/typescript
│ │ ├── typescript-eslint -> .pnpm/typescript-eslint@8.44.0_eslint@9.36.0_typescript@5.8.3/node_modules/typescript-eslint
│ │ ├── vite -> .pnpm/vite@7.1.6/node_modules/vite
│ │ └── @vitejs
│ │ └── plugin-react -> ../.pnpm/@vitejs+plugin-react@5.0.3_vite@7.1.6/node_modules/@vitejs/plugin-react
│ ├── package.json
│ ├── pnpm-lock.yaml
│ ├── public
│ │ └── vite.svg
│ ├── README.md
│ ├── src
│ │ ├── App.css
│ │ ├── App.tsx
│ │ ├── assets
│ │ │ └── react.svg
│ │ ├── components
│ │ │ ├── ChampionAbilities.tsx
│ │ │ ├── ChampionRelationships.tsx
│ │ │ └── ChampionSkins.tsx
│ │ ├── index.css
│ │ ├── lib
│ │ │ └── api.ts
│ │ ├── main.tsx
│ │ ├── pages
│ │ │ ├── ChampionDetail.tsx
│ │ │ └── champions.tsx
│ │ └── vite-env.d.ts
│ ├── tsconfig.app.json
│ ├── tsconfig.json
│ ├── tsconfig.node.json
│ └── vite.config.ts
└── tests
└── test_api.py

39 directories, 53 files
(so far)

---

## 5. Workflow

1. Define/update Pydantic models in backend.
2. Implement API routes with full error handling.
3. Update `src/lib/api.ts` to reflect new contract.
4. Update frontend components/pages to consume API.
5. Write tests for backend + frontend.
6. Commit + push — no merges until all checks pass.

---

## 6. Pull Request Rules

- ✅ Lint + tests must pass
- ✅ Docstrings present
- ✅ Riot-standard structure followed
