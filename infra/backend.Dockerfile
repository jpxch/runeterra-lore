FROM python:3.12.6-slim

RUN useradd -ms /bin/bash appuser

WORKDIR /app/backend

RUN pip install --no-cache-dir poetry==1.8.3
COPY backend/pyproject.toml backend/poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY backend /app/backend/

USER appuser

EXPOSE 8000

WORKDIR /app
CMD ["python", "-m", "backend.run"]