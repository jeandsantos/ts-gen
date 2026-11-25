# ts-gen

Time series generator for Python

## Usage

Build an immutable recipe by chaining `add`, then generate a series from it.
Every recipe starts from zero, so a baseline is an explicit `ConstantTrend`.

```python
from ts_gen import ConstantTrend, LinearTrend, Recipe

recipe = (
    Recipe()
    .add(ConstantTrend(value=100.0), name="baseline")
    .add(LinearTrend(intercept=0.0, slope=10.0, per="1d"), name="growth")
)
result = recipe.generate(start="2024-01-01", end="2024-01-08", step="1h", seed=42)
result.observed  # pandas Series indexed by timestamp
result.seed  # effective seed
```

- The grid includes `start` and excludes `end`.
- An interval shorter than one step yields only `start`.
- `step` is a positive integer multiple of seconds, minutes, or hours (`"30s"`, `"15min"`, `"2h"`).
- Ranges must be timezone-naive.
- `LinearTrend` slopes are per fixed elapsed duration, measured from `start`.
- `per` accepts s, min, h, d (24 hours), and w (7 days).
- Changing `step` does not change trend values at shared timestamps.
- `add` returns a new recipe and leaves the original unchanged.
- Operation names must be unique within a recipe.
- Omitting `seed` draws a fresh one, exposed as `result.seed`.
- Invalid inputs raise `ts_gen.ValidationError`.

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
