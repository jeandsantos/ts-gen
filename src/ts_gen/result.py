from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class GenerationResult:
    """The outcome of generating a recipe.

    ``observed`` is the synthetic series indexed by timestamp; ``seed`` is the effective seed, which reproduces
    the run when passed back to ``Recipe.generate``.
    """

    observed: pd.Series
    seed: int
