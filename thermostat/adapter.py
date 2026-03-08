"""Thermostat adapter abstraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ThermostatAdapter:
    """Simple proportional controller wrapper for thermostat-like logic."""

    max_power_kw: float
    kp: float = 0.75

    def __post_init__(self) -> None:
        self._state: dict[str, Any] = {
            "indoor_temperature": 20.0,
            "target_temperature": 21.0,
            "time_of_day": 0,
            "occupancy": True,
            "external_temperature": 10.0,
        }

    def update(self, sensor_data: dict[str, Any]) -> None:
        self._state.update(sensor_data)

    def compute_heating_command(self) -> float:
        target = float(self._state["target_temperature"])
        indoor = float(self._state["indoor_temperature"])
        occupancy = bool(self._state.get("occupancy", True))
        setback = 1.0 if not occupancy else 0.0
        error = max(0.0, (target - setback) - indoor)
        command = min(self.max_power_kw, self.kp * error * self.max_power_kw)
        return max(0.0, command)
