.PHONY: test test-backend test-frontend lint lint-backend lint-frontend typecheck typecheck-backend typecheck-frontend

all: lint typecheck test

test: test-backend test-frontend

test-backend:
	poetry run pytest backend/tests -v --maxfail=1 --disable-warnings

test-frontend:
	frontend && pnpm test

lint: lint-backend lint-frontend

lint-backend:
	poetry run black --check backend
	poetry run isort ---check-only backend

lint-frontend:
	frontend && pnpm lint

typecheck: typecheck-backend typecheck-frontend

typecheck-backend:
	poetry run mypy backend

typecheck-frontend:e
	frontend && pnpm typecheck