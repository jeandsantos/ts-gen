"""Fixed-duration time grids and the duration strings that describe them."""

from __future__ import annotations

import re
from collections.abc import Collection
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import StrEnum

import pandas as pd

from ts_gen.errors import ValidationError


class TimeUnit(StrEnum):
    """A fixed elapsed unit; a day is always 24 hours and a week 7 x 24 hours."""

    SECOND = "s"
    MINUTE = "min"
    HOUR = "h"
    DAY = "d"
    WEEK = "w"

    @property
    def length(self) -> timedelta:
        return _UNIT_LENGTHS[self]

    @classmethod
    def from_alias(cls, alias: str) -> TimeUnit | None:
        try:
            return cls(alias)
        except ValueError:
            return None


_UNIT_LENGTHS = {
    TimeUnit.SECOND: timedelta(seconds=1),
    TimeUnit.MINUTE: timedelta(minutes=1),
    TimeUnit.HOUR: timedelta(hours=1),
    TimeUnit.DAY: timedelta(hours=24),
    TimeUnit.WEEK: timedelta(days=7),
}

STEP_UNITS = frozenset({TimeUnit.SECOND, TimeUnit.MINUTE, TimeUnit.HOUR})
"""Units accepted for sampling steps."""

RATE_UNITS = frozenset(TimeUnit)
"""Units accepted for elapsed trend rates."""


@dataclass(frozen=True)
class Duration:
    """A positive integer multiple of a fixed elapsed unit, written like ``"15min"``."""

    count: int
    unit: TimeUnit

    _PATTERN = re.compile(r"^\s*(?P<count>[^a-zA-Z\s]*)\s*(?P<unit>[a-zA-Z]*)\s*$")

    @classmethod
    def parse(cls, text: object, *, label: str, kind: str, allowed: Collection[TimeUnit]) -> Duration:
        if not isinstance(text, str):
            raise ValidationError(f"{label} must be a string such as '15min', got {text!r}")
        match = cls._PATTERN.match(text)
        count = match["count"] if match else ""
        if match is None or not (count.isascii() and count.isdigit()) or int(count) <= 0:
            raise ValidationError(f"{label} {text!r} must be a positive integer followed by a unit, e.g. '15min'")
        unit = TimeUnit.from_alias(match["unit"])
        if unit is None or unit not in allowed:
            supported = ", ".join(sorted(allowed))
            raise ValidationError(
                f"{label} {text!r} has unsupported {kind} unit {match['unit']!r}; supported units: {supported}"
            )
        return cls(count=int(count), unit=unit)

    def to_timedelta(self) -> pd.Timedelta:
        try:
            delta = pd.Timedelta(self.count * self.unit.length)
        except (OverflowError, ValueError) as error:
            raise ValidationError(
                f"duration {self.count}{self.unit.value} exceeds the supported timedelta range"
            ) from error
        assert isinstance(delta, pd.Timedelta)
        return delta


@dataclass(frozen=True)
class TimeGrid:
    """Start-anchored timestamps from ``start`` (inclusive) to ``end`` (exclusive), with elapsed time from start."""

    index: pd.DatetimeIndex
    elapsed: pd.TimedeltaIndex

    @classmethod
    def build(cls, start: str | datetime, end: str | datetime, step: str) -> TimeGrid:
        start_ts = cls._to_timestamp(start, label="start")
        end_ts = cls._to_timestamp(end, label="end")
        if start_ts.tzinfo is not None or end_ts.tzinfo is not None:
            raise ValidationError(
                "start and end must both be timezone-naive; timezone-aware ranges are not supported yet "
                f"(got start={start_ts}, end={end_ts})"
            )
        if start_ts >= end_ts:
            raise ValidationError(f"start must be before end (got start={start_ts}, end={end_ts})")
        step_delta = Duration.parse(step, label="step", kind="step", allowed=STEP_UNITS).to_timedelta()
        index = pd.date_range(start=start_ts, end=end_ts, freq=step_delta, inclusive="left", name="timestamp")
        return cls(index=index, elapsed=pd.TimedeltaIndex(index - start_ts))

    @staticmethod
    def _to_timestamp(value: object, *, label: str) -> pd.Timestamp:
        try:
            timestamp = pd.Timestamp(value)  # ty: ignore[invalid-argument-type]
        except (TypeError, ValueError) as error:
            raise ValidationError(f"{label} {value!r} is not a valid timestamp") from error
        if not isinstance(timestamp, pd.Timestamp):
            raise ValidationError(f"{label} {value!r} is not a valid timestamp")
        return timestamp
