## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues for `jeandsantos/ts-gen`. Before reading or publishing tickets, read `docs/agents/issue-tracker.md`.

### Triage labels

Use the five default triage labels. Before triaging or applying triage labels, read `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout. Before exploring domain concepts or proposing architectural changes, read `docs/agents/domain.md`.

## Development commands

The environment is managed with uv; never use `pip` directly. Add dependencies with `uv add <pkg>` (or `uv add --dev <pkg>`) so `uv.lock` stays in sync.

- Tests: `uv run pytest` (single file: `uv run pytest tests/path/test_x.py`)
- Type-check: `uv run ty check`
- Lint/format: `uv run ruff check --fix` and `uv run ruff format`
- All hooks: `uv run prek run --all-files`

## Commits

When making changes, commit each coherent, verified milestone and follow `docs/agents/commit-guidelines.md` for commit cadence and message format.
