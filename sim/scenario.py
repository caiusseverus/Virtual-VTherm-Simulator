"""Scenario model and YAML loader."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any


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


def _load_yaml(path: str) -> dict[str, Any]:
    try:
        import yaml  # type: ignore

        with open(path, "r", encoding="utf-8") as file:
            loaded = yaml.safe_load(file) or {}
        return loaded if isinstance(loaded, dict) else {}
    except Exception:
        return _parse_simple_yaml(path)


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
    building_heat_capacity: float
    heat_loss_coefficient: float
    heating_power_kw: float
    solar_gain_kw: float = 0.0
    internal_heat_gain_kw: float = 0.0

    @classmethod
    def from_yaml(cls, path: str) -> "SimulationScenario":
        data = _load_yaml(path)

        if "simulation" in data:
            sim = data.get("simulation", {})
            building = data.get("building", {})
            heating = data.get("heating", {})
            weather = data.get("weather", {})
            thermostat = data.get("thermostat", {})
            gains = data.get("gains", {})

            return cls(
                name=str(data.get("name", "simulation")),
                start_time=datetime.fromisoformat(str(data.get("start_time", "2025-01-01T00:00:00"))),
                duration=timedelta(hours=float(sim.get("duration_hours", 24))),
                step_seconds=int(sim.get("timestep_seconds", 60)),
                indoor_initial_c=float(sim.get("initial_indoor_temp", 19.0)),
                target_temp_c=float(thermostat.get("target_temperature", 21.0)),
                outdoor_base_c=float(weather.get("outdoor_base_c", 5.0)),
                outdoor_amplitude_c=float(weather.get("outdoor_amplitude_c", 4.0)),
                building_heat_capacity=float(building.get("heat_capacity", 30_000_000)),
                heat_loss_coefficient=float(building.get("heat_loss_coefficient", 200)),
                heating_power_kw=float(heating.get("max_power_kw", 12)),
                solar_gain_kw=float(gains.get("solar_gain_kw", 0.0)),
                internal_heat_gain_kw=float(gains.get("internal_heat_gain_kw", 0.0)),
            )

        return cls(
            name=data["name"],
            start_time=datetime.fromisoformat(str(data["start_time"])),
            duration=timedelta(hours=float(data["duration_hours"])),
            step_seconds=int(data.get("step_seconds", 60)),
            indoor_initial_c=float(data["indoor_initial_c"]),
            target_temp_c=float(data["target_temp_c"]),
            outdoor_base_c=float(data["outdoor_base_c"]),
            outdoor_amplitude_c=float(data.get("outdoor_amplitude_c", 0.0)),
            building_heat_capacity=float(data.get("building_heat_capacity", data.get("thermal_mass_j_per_c", 30_000_000))),
            heat_loss_coefficient=float(data.get("heat_loss_coefficient", data.get("heat_loss_w_per_c", 200))),
            heating_power_kw=float(data.get("heating_power_kw", float(data.get("max_heating_power_w", 12_000)) / 1000.0)),
            solar_gain_kw=float(data.get("solar_gain_kw", 0.0)),
            internal_heat_gain_kw=float(data.get("internal_heat_gain_kw", 0.0)),
        )
