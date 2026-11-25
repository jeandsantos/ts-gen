from datetime import datetime

import pytest

from ts_gen import ConstantTrend, LinearTrend, Recipe


@pytest.fixture
def day_range() -> dict[str, datetime]:
    return {"start": datetime(2024, 1, 1), "end": datetime(2024, 1, 2)}


@pytest.fixture
def short_range() -> dict[str, datetime]:
    return {"start": datetime(2024, 1, 1, 0), "end": datetime(2024, 1, 1, 3)}


@pytest.fixture
def empty_recipe() -> Recipe:
    return Recipe()


@pytest.fixture
def trend_recipe() -> Recipe:
    return (
        Recipe()
        .add(ConstantTrend(value=10.0), name="baseline")
        .add(LinearTrend(intercept=1.0, slope=2.0, per="1h"), name="growth")
    )
