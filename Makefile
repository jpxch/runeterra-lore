.PHONY: test test-backend test-frontend lint docker-build docker-up docker-down

test-backend:
	poetry run pytest /backend/tests -v --maxfail=1 --disable-warnings

test-frontend:
	cd frontend && pnpm test

test: test-backend test-frontend

lint-backend:
	poetry run black backend --check
	poetry run isort backend --check
	poetry run flake8 backend

lint-frontend:
	cd frontend && pnpm lint

lint: lint-backend lint-frontend

docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down