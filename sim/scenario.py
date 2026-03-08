"""Scenario model and YAML loader."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


def _parse_simple_yaml(path: str) -> dict[str, str]:
    data: dict[str, str] = {}
    with open(path, "r", encoding="utf-8") as file:
        for raw in file:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            key, sep, value = line.partition(":")
            if not sep:
                continue
            data[key.strip()] = value.strip().strip('"').strip("'")
    return data


@dataclass
class SimulationScenario:
    """All fixed configuration required to run one simulation."""

    name: str
    start_time: datetime
    duration: timedelta
    step_seconds: int
    indoor_initial_c: float
    target_temp_c: float
    outdoor_base_c: float
    outdoor_amplitude_c: float
    thermal_mass_j_per_c: float
    heat_loss_w_per_c: float
    max_heating_power_w: float

    @classmethod
    def from_yaml(cls, path: str) -> "SimulationScenario":
        data = _parse_simple_yaml(path)

        return cls(
            name=data["name"],
            start_time=datetime.fromisoformat(data["start_time"]),
            duration=timedelta(hours=float(data["duration_hours"])),
            step_seconds=int(data.get("step_seconds", 60)),
            indoor_initial_c=float(data["indoor_initial_c"]),
            target_temp_c=float(data["target_temp_c"]),
            outdoor_base_c=float(data["outdoor_base_c"]),
            outdoor_amplitude_c=float(data.get("outdoor_amplitude_c", 0.0)),
            thermal_mass_j_per_c=float(data["thermal_mass_j_per_c"]),
            heat_loss_w_per_c=float(data["heat_loss_w_per_c"]),
            max_heating_power_w=float(data["max_heating_power_w"]),
        )
