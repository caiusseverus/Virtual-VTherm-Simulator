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
