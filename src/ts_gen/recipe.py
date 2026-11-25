from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

import numpy as np
import pandas as pd

from ts_gen.errors import ValidationError
from ts_gen.grid import TimeGrid
from ts_gen.operations import Operation
from ts_gen.result import GenerationResult


@dataclass(frozen=True)
class Recipe:
    """An immutable, ordered composition of named operations that starts from zero.

    Build recipes by chaining ``add``; each call returns a new recipe. Generate with ``generate``, which never
    mutates the recipe, so one recipe can be reused across ranges, steps, and seeds.
    """

    operations: tuple[tuple[str, Operation], ...] = ()

    def add(self, operation: Operation, *, name: str) -> Recipe:
        """Return a new recipe with ``operation`` appended under ``name``; this recipe is unchanged."""
        if not isinstance(operation, Operation):
            raise ValidationError(f"operation must be an ts_gen Operation, got {operation!r}")
        if not isinstance(name, str) or not name.strip():
            raise ValidationError(f"name must be a non-empty string, got {name!r}")
        if any(existing == name for existing, _ in self.operations):
            raise ValidationError(f"operation name {name!r} is already used in this recipe; names must be unique")
        return Recipe(operations=(*self.operations, (name, operation)))

    def generate(
        self, *, start: str | datetime, end: str | datetime, step: str, seed: int | None = None
    ) -> GenerationResult:
        """Evaluate the recipe on the grid from ``start`` (inclusive) to ``end`` (exclusive) every ``step``.

        ``step`` is a positive integer multiple of seconds, minutes, or hours, e.g. ``"15min"``. Elapsed time
        is measured from ``start``. Omitting ``seed`` draws a fresh one, exposed as ``result.seed``.
        """
        effective_seed = _resolve_seed(seed)
        grid = TimeGrid.build(start, end, step)
        values = np.zeros(len(grid.index))
        for _, operation in self.operations:
            values = operation.apply(values, grid)
        return GenerationResult(observed=pd.Series(values, index=grid.index, name="value"), seed=effective_seed)


def _resolve_seed(seed: object) -> int:
    if seed is None:
        entropy = np.random.SeedSequence().entropy
        assert isinstance(entropy, int)
        return entropy
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValidationError(f"seed must be a non-negative integer or None, got {seed!r}")
    return seed
