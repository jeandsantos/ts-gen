import pandas as pd
import pytest

from ts_gen import ConstantTrend, Recipe, ValidationError


class TestRecipeGenerate:
    def test_generate_empty_recipe_yields_zeros(self, empty_recipe: Recipe, short_range: dict) -> None:
        result = empty_recipe.generate(**short_range, step="1h")

        assert list(result.observed.index) == [
            pd.Timestamp("2024-01-01 00:00"),
            pd.Timestamp("2024-01-01 01:00"),
            pd.Timestamp("2024-01-01 02:00"),
        ]
        assert result.observed.tolist() == [0.0, 0.0, 0.0]

    def test_generate_constant_and_linear_contributions_sum(self, trend_recipe: Recipe, short_range: dict) -> None:
        result = trend_recipe.generate(**short_range, step="1h")

        assert result.observed.tolist() == [11.0, 13.0, 15.0]

    def test_generate_slope_is_independent_of_step(self, trend_recipe: Recipe, day_range: dict) -> None:
        hourly = trend_recipe.generate(**day_range, step="1h").observed
        quarter_hourly = trend_recipe.generate(**day_range, step="15min").observed

        pd.testing.assert_series_equal(quarter_hourly.loc[hourly.index], hourly, check_freq=False)
        assert quarter_hourly.loc["2024-01-01 00:15"] == 11.5

    def test_generate_interval_shorter_than_step_yields_start_only(self, trend_recipe: Recipe) -> None:
        result = trend_recipe.generate(start="2024-01-01 00:00", end="2024-01-01 00:30", step="1h")

        assert list(result.observed.index) == [pd.Timestamp("2024-01-01 00:00")]
        assert result.observed.tolist() == [11.0]

    def test_generate_accepts_step_multiples_of_seconds_minutes_and_hours(self, empty_recipe: Recipe) -> None:
        start, end = "2024-01-01 00:00:00", "2024-01-01 06:00:00"

        assert len(empty_recipe.generate(start=start, end=end, step="90s").observed) == 240
        assert len(empty_recipe.generate(start=start, end=end, step="45min").observed) == 8
        assert len(empty_recipe.generate(start=start, end=end, step="2h").observed) == 3

    def test_generate_reuses_recipe_across_ranges(self, trend_recipe: Recipe, short_range: dict) -> None:
        first = trend_recipe.generate(**short_range, step="1h").observed
        trend_recipe.generate(start="2025-06-01", end="2025-06-02", step="1min")
        second = trend_recipe.generate(**short_range, step="1h").observed

        pd.testing.assert_series_equal(first, second)


class TestRecipeAdd:
    def test_add_leaves_original_recipe_unchanged(self, empty_recipe: Recipe, short_range: dict) -> None:
        extended = empty_recipe.add(ConstantTrend(value=5.0), name="baseline")

        assert empty_recipe.generate(**short_range, step="1h").observed.tolist() == [0.0, 0.0, 0.0]
        assert extended.generate(**short_range, step="1h").observed.tolist() == [5.0, 5.0, 5.0]


class TestRecipeGenerateSeed:
    def test_generate_exposes_explicit_seed(self, trend_recipe: Recipe, short_range: dict) -> None:
        result = trend_recipe.generate(**short_range, step="1h", seed=42)

        assert result.seed == 42

    def test_generate_assigns_fresh_seed_when_omitted(self, trend_recipe: Recipe, short_range: dict) -> None:
        first = trend_recipe.generate(**short_range, step="1h")
        second = trend_recipe.generate(**short_range, step="1h")

        assert isinstance(first.seed, int)
        assert first.seed >= 0
        assert first.seed != second.seed

    def test_generate_result_carries_no_diagnostics(self, trend_recipe: Recipe, short_range: dict) -> None:
        result = trend_recipe.generate(**short_range, step="1h", seed=1)

        for diagnostic in ("reference", "events", "stages"):
            assert not hasattr(result, diagnostic)


class TestRecipeGenerateValidation:
    @pytest.mark.parametrize(
        ("start", "end"),
        [("2024-01-02", "2024-01-01"), ("2024-01-01", "2024-01-01")],
        ids=["start-after-end", "start-equals-end"],
    )
    def test_generate_rejects_start_not_before_end(self, empty_recipe: Recipe, start: str, end: str) -> None:
        with pytest.raises(ValidationError, match="start must be before end"):
            empty_recipe.generate(start=start, end=end, step="1h")

    @pytest.mark.parametrize(
        ("step", "message"),
        [
            ("0h", "positive integer"),
            ("-1h", "positive integer"),
            ("1.5h", "positive integer"),
            ("h", "positive integer"),
            ("²h", "positive integer"),
            ("1d", "unsupported step unit 'd'"),
            ("1hour", "unsupported step unit 'hour'"),
            ("1month", "unsupported step unit 'month'"),
            ("1fortnight", "unsupported step unit 'fortnight'"),
        ],
    )
    def test_generate_rejects_invalid_step(
        self, empty_recipe: Recipe, day_range: dict, step: str, message: str
    ) -> None:
        with pytest.raises(ValidationError, match=message):
            empty_recipe.generate(**day_range, step=step)

    def test_generate_rejects_mixed_naive_and_aware_endpoints(self, empty_recipe: Recipe) -> None:
        with pytest.raises(ValidationError, match="timezone-naive"):
            empty_recipe.generate(start="2024-01-01", end="2024-01-02T00:00+01:00", step="1h")

    def test_generate_rejects_aware_endpoints(self, empty_recipe: Recipe) -> None:
        with pytest.raises(ValidationError, match="timezone-naive"):
            empty_recipe.generate(start="2024-01-01T00:00Z", end="2024-01-02T00:00Z", step="1h")

    def test_generate_rejects_unparseable_endpoint(self, empty_recipe: Recipe) -> None:
        with pytest.raises(ValidationError, match="start"):
            empty_recipe.generate(start="not a date", end="2024-01-02", step="1h")

    @pytest.mark.parametrize("seed", [-1, 1.5, True, "42"])
    def test_generate_rejects_invalid_seed(self, empty_recipe: Recipe, day_range: dict, seed: object) -> None:
        with pytest.raises(ValidationError, match="seed"):
            empty_recipe.generate(**day_range, step="1h", seed=seed)  # ty: ignore[invalid-argument-type]


class TestRecipeAddValidation:
    def test_add_rejects_duplicate_name(self, trend_recipe: Recipe) -> None:
        with pytest.raises(ValidationError, match="'growth' is already used"):
            trend_recipe.add(ConstantTrend(value=1.0), name="growth")

    @pytest.mark.parametrize("name", ["", "   ", 3])
    def test_add_rejects_invalid_name(self, empty_recipe: Recipe, name: object) -> None:
        with pytest.raises(ValidationError, match="name"):
            empty_recipe.add(ConstantTrend(value=1.0), name=name)  # ty: ignore[invalid-argument-type]

    def test_add_rejects_non_operation(self, empty_recipe: Recipe) -> None:
        with pytest.raises(ValidationError, match="operation"):
            empty_recipe.add(5.0, name="baseline")  # ty: ignore[invalid-argument-type]
