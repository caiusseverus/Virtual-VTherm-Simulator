"""Metrics recording for simulation runs."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class MiniDataFrame:
    """Tiny DataFrame-like structure used to avoid heavy runtime dependency."""

    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self.rows = rows

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, key: str) -> list[Any]:
        return [row[key] for row in self.rows]


@dataclass
class MetricsSummary:
    temperature_tracking_error: float
    heating_duty_cycle: float
    overshoot_degrees: float
    energy_usage_kwh: float
    comfort_violation_time_hours: float


@dataclass
class MetricsRecorder:
    """Accumulates timestep metrics and exports CSV."""

    _rows: list[dict[str, Any]] = field(default_factory=list)

    def record(
        self,
        time_s: float,
        indoor_temperature: float,
        outdoor_temperature: float,
        target_temperature: float,
        heating_output: float,
        energy_consumption_kwh: float,
    ) -> None:
        self._rows.append(
            {
                "time_s": time_s,
                "indoor_temperature": indoor_temperature,
                "outdoor_temperature": outdoor_temperature,
                "target_temperature": target_temperature,
                "heating_output": heating_output,
                "energy_consumption": energy_consumption_kwh,
            }
        )

    def to_dataframe(self) -> MiniDataFrame:
        return MiniDataFrame(self._rows)

    def summarize(self, step_seconds: float) -> MetricsSummary:
        return summarize(self._rows, step_seconds)

    def save_csv(self, path: str | Path) -> Path:
        output = Path(path)
        output.parent.mkdir(parents=True, exist_ok=True)
        if not self._rows:
            output.write_text("", encoding="utf-8")
            return output
        with output.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(self._rows[0].keys()))
            writer.writeheader()
            writer.writerows(self._rows)
        return output


def summarize(rows: list[dict[str, Any]], step_seconds: float) -> MetricsSummary:
    if not rows:
        raise ValueError("Cannot summarize empty rows")

    abs_errors = [abs(float(r["indoor_temperature"]) - float(r["target_temperature"])) for r in rows]
    mean_error = sum(abs_errors) / len(abs_errors)

    heating_values = [float(r["heating_output"]) for r in rows]
    duty_cycle = sum(1.0 for value in heating_values if value > 0.0) / len(heating_values)

    overshoot = max(max(float(r["indoor_temperature"]) - float(r["target_temperature"]), 0.0) for r in rows)
    energy_kwh = float(rows[-1]["energy_consumption"])
    violation_hours = sum(1 for e in abs_errors if e > 0.5) * step_seconds / 3600.0

    return MetricsSummary(
        temperature_tracking_error=mean_error,
        heating_duty_cycle=duty_cycle,
        overshoot_degrees=overshoot,
        energy_usage_kwh=energy_kwh,
        comfort_violation_time_hours=violation_hours,
    )
