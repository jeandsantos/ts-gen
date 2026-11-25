# ts-gen

Time series generator for Python

## Development

This project uses [uv](https://docs.astral.sh/uv/) for environment and dependency management, and
[prek](https://github.com/j178/prek) to run the hooks in `.pre-commit-config.yaml`.

```bash
uv sync                      # create .venv and install the package with dev dependencies
uv run prek install          # install the git pre-commit hook
uv run pytest                # run the test suite
uv run ruff check --fix      # lint
uv run ruff format           # format
uv run ty check              # type-check
uv run prek run --all-files  # run every hook against the whole repository
```
