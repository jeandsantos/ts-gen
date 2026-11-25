import math
from numbers import Real

from ts_gen.errors import ValidationError


def require_finite(value: object, *, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
        raise ValidationError(f"{label} must be a finite real number, got {value!r}")
    return float(value)
