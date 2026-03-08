"""Metrics computation for simulation runs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class MetricsSummary:
    temperature_tracking_error: float
    heating_duty_cycle: float
    overshoot_degrees: float
    energy_usage_kwh: float
    comfort_violation_time_hours: float


def summarize(rows: list[dict[str, Any]], step_seconds: int) -> MetricsSummary:
    if not rows:
        raise ValueError("Cannot summarize empty rows")

    abs_errors = [abs(float(r["indoor_temperature"]) - float(r["target_temperature"])) for r in rows]
    mean_error = sum(abs_errors) / len(abs_errors)

    heating_values = [float(r["heating_power_kw"]) for r in rows]
    max_power = max(max(heating_values), 1e-9)
    duty_cycle = sum(1.0 for value in heating_values if value > 0.0) / len(heating_values)

    overshoot = max(max(float(r["indoor_temperature"]) - float(r["target_temperature"]), 0.0) for r in rows)
    energy_kwh = sum(value * step_seconds / 3600.0 for value in heating_values)
    violation_hours = sum(1 for e in abs_errors if e > 0.5) * step_seconds / 3600.0

    return MetricsSummary(
        temperature_tracking_error=mean_error,
        heating_duty_cycle=duty_cycle,
        overshoot_degrees=overshoot,
        energy_usage_kwh=energy_kwh,
        comfort_violation_time_hours=violation_hours,
    )
