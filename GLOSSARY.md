# Synthetic Time Series

Synthetic time series combine controlled temporal patterns and disturbances for forecasting and anomaly-detection experiments.

## Language

**Series**:
A sequence of numeric observations associated with timestamps for one variable.

**Recipe**:
A reusable description of a synthetic series as an ordered composition of components and transformations.

**Group**:
A locally composed signal added as a contribution to a larger recipe, allowing effects to be scoped to that contribution.

**Time grid**:
The ordered timestamps at which a synthetic series has observations.

**Time origin**:
The reference instant from which a temporal pattern's elapsed position is measured.

**Component**:
A contribution to a synthetic series, such as a trend, seasonal pattern, cyclical pattern, or additive noise.

**Transformation**:
An operation applied to an existing signal, whose position relative to other operations can affect the resulting series.

**Seasonality**:
A repeating pattern tied to a known calendar or fixed period.
_Avoid_: Cyclicality for fixed-period repetition

**Cyclicality**:
An oscillating pattern whose period can vary and need not align with the calendar.
_Avoid_: Seasonality for variable-period oscillations

**Regime change**:
A persistent change in a series' level, slope, or variance.
_Avoid_: Concept drift when no input-target relationship is modeled

**Missingness**:
The absence of an observed value at a retained timestamp.
_Avoid_: Dropped timestamps, irregular sampling

**Noise**:
Random variation included as part of a series' expected behavior, rather than labeled as an injected anomaly.

**Injected anomaly**:
A deliberately introduced perturbation designated as anomalous in a synthetic series.

**Point anomaly**:
An additive offset introduced at a selected observation.

**Level change**:
A persistent additive offset beginning at a selected time.

**Slope change**:
A persistent change in the rate of a series, beginning continuously at a selected time.

**Variance change**:
A persistent scaling of deviations around a declared center, intended to alter a noise contribution's variance.

**Periodic burst**:
An additive offset active within a bounded window that repeats on a defined schedule.

**Reference series**:
The series a recipe produces with its declared anomaly injections omitted and the same ordinary random draws retained.
_Avoid_: Noiseless series, pre-anomaly signal
