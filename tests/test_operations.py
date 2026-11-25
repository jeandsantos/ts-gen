import math

import pytest

from ts_gen import ConstantTrend, LinearTrend, Recipe, ValidationError


class TestConstantTrend:
    @pytest.mark.parametrize("value", [math.nan, math.inf, "10", True, None])
    def test_constant_trend_rejects_invalid_value(self, value: object) -> None:
        with pytest.raises(ValidationError, match="value"):
            ConstantTrend(value=value)  # ty: ignore[invalid-argument-type]


class TestLinearTrend:
    def test_linear_trend_per_day_means_24_hours(self) -> None:
        recipe = Recipe().add(LinearTrend(intercept=0.0, slope=10.0, per="1d"), name="growth")

        result = recipe.generate(start="2024-01-01", end="2024-01-03", step="12h")

        assert result.observed.tolist() == [0.0, 5.0, 10.0, 15.0]

    def test_linear_trend_per_week_means_seven_days(self) -> None:
        recipe = Recipe().add(LinearTrend(intercept=0.0, slope=7.0, per="1w"), name="growth")

        result = recipe.generate(start="2024-01-01", end="2024-01-02", step="12h")

        assert result.observed.tolist() == [0.0, 0.5]

    @pytest.mark.parametrize(
        ("kwargs", "message"),
        [
            ({"intercept": math.nan, "slope": 1.0, "per": "1h"}, "intercept"),
            ({"intercept": 0.0, "slope": math.inf, "per": "1h"}, "slope"),
            ({"intercept": 0.0, "slope": 1.0, "per": "0h"}, "positive integer"),
            ({"intercept": 0.0, "slope": 1.0, "per": "1month"}, "unsupported rate unit 'month'"),
            ({"intercept": 0.0, "slope": 1.0, "per": 3600}, "per"),
        ],
    )
    def test_linear_trend_rejects_invalid_parameters(self, kwargs: dict, message: str) -> None:
        with pytest.raises(ValidationError, match=message):
            LinearTrend(**kwargs)
