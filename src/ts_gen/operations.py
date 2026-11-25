"""Built-in recipe operations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from ts_gen.grid import RATE_UNITS, Duration, TimeGrid
from ts_gen.validation import require_finite


class Operation(ABC):
    """A step in a recipe that maps the current signal to a new signal."""

    @abstractmethod
    def apply(self, values: np.ndarray, grid: TimeGrid) -> np.ndarray: ...


@dataclass(frozen=True)
class ConstantTrend(Operation):
    """Adds a constant ``value`` at every timestamp."""

    value: float

    def __post_init__(self) -> None:
        require_finite(self.value, label="ConstantTrend value")

    def apply(self, values: np.ndarray, grid: TimeGrid) -> np.ndarray:
        return values + self.value


@dataclass(frozen=True)
class LinearTrend(Operation):
    """Adds ``intercept + slope * elapsed / per``.

    ``per`` is a fixed elapsed duration such as ``"1h"`` or ``"1d"`` (24 hours), so the trend's values at a
    timestamp do not depend on the sampling step.
    """

    intercept: float
    slope: float
    per: str
    _per_delta: pd.Timedelta = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        require_finite(self.intercept, label="LinearTrend intercept")
        require_finite(self.slope, label="LinearTrend slope")
        per_delta = Duration.parse(self.per, label="LinearTrend per", kind="rate", allowed=RATE_UNITS).to_timedelta()
        object.__setattr__(self, "_per_delta", per_delta)

    def apply(self, values: np.ndarray, grid: TimeGrid) -> np.ndarray:
        rate_units = np.asarray(grid.elapsed / self._per_delta, dtype=float)
        return values + self.intercept + self.slope * rate_units
