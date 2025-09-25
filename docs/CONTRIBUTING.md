# Contributing

Thanks for helping build **Runeterra Lore**! This guide outlines how to propose changes with Riot-quality standards.

## Ground Rules
- Be kind, specific, and constructive in reviews.
- Prefer small, focused PRs (≤ 400 lines changed).
- Add/Update tests with every behavioral change.

## Development Flow
1. Create a branch: `git checkout -b feature/my-feature`.
2. Run locally: `make dev`.
3. Ensure all checks pass:
   - `make lint`
   - `make typecheck`
   - `make test`
4. Commit using Conventional Commits:
   - `feat: add champion timeline view`
   - `fix(api): correct skin relation mapping`
5. Open a PR with:
   - Problem statement
   - Solution overview
   - Screenshots (UI) / Example requests (API)
   - Risks & roll-back plan

## Code Style
- Python: Black, isort, mypy (strict)
- JS/TS: ESLint, Prettier, TypeScript strict
- Keep functions small; document public APIs.

## Security & Secrets
- Never commit secrets. Use `VAULT_` env references.
- Use parameterized queries and validate all inputs.

## Testing
- Unit + integration tests for backend routes.
- Snapshot & accessibility tests for UI.
- Contract tests against `API_SPEC.yaml`.

## Review Checklist (PR Author)
- [ ] Linted & formatted
- [ ] Tests added/updated
- [ ] API docs updated (if changed)
- [ ] No secrets in diff
- [ ] Backward compatibility considered

## Review Checklist (Reviewer)
- [ ] Clear problem/solution
- [ ] Correctness & edge cases
- [ ] Performance & security
- [ ] Tests meaningful
- [ ] Naming & readability
