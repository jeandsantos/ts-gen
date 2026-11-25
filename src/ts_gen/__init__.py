"""Composable synthetic time-series generation."""

from importlib.metadata import version

from ts_gen.errors import ValidationError
from ts_gen.operations import ConstantTrend, LinearTrend, Operation
from ts_gen.recipe import Recipe
from ts_gen.result import GenerationResult

__version__ = version("ts-gen")

__all__ = ["ConstantTrend", "GenerationResult", "LinearTrend", "Operation", "Recipe", "ValidationError", "__version__"]
