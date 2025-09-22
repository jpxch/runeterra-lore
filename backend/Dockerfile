FROM python:3.12.6-slim AS base

RUN useradd -ms /bin/bash appuser

WORKDIR /app

RUN pip install --no-cache-dir poetry==1.8.3
COPY backend/pyproject.toml backend/poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --without dev

COPY backend /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "${UVICORN_HOST}", "--port", "${UVICORN_PORT}"]