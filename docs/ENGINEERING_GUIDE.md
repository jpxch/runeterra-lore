# Engineering Guide

## Coding Standards
- Follow PEP8 (Python) and Riot's ESLint rules (JavaScript/TypeScript).
- Strict type hints enforced.
- No hardcoded values, especially secrets.
- Meaningful logging with correlation IDs for requests.

## Testing
- Every API endpoint must have unit + integration tests.
- Target coverage: **90%+**.
- Snapshot tests for UI components.
- Contract tests against `API_SPEC.yaml`.

## Security
- Secrets managed via Riot's Vault service.
- Never commit `.env` files to source control.
- All endpoints require auth in staging/production.
- Regular dependency scanning; fix criticals before release.

## Review Process
- PRs require at least **1 reviewer** from the feature team.
- No direct pushes to `main`.
- All merges go through CI/CD with lint + tests + type checks.

## Branching
- `main` → protected, release-ready
- `develop` → integration branch (optional)
- `feature/*`, `fix/*`, `chore/*`
