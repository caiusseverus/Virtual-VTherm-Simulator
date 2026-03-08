"""Adapter around thermostat logic for offline simulation.

Tries to import versatile_thermostat if available, otherwise uses a deterministic
hysteresis controller compatible with thermostat demand semantics.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ThermostatAdapter:
    """Offline thermostat adapter producing heating demand in [0, 1]."""

    target_temperature: float
    hysteresis: float = 0.2
    _heating_on: bool = False

    def set_temperature(self, target: float) -> None:
        self.target_temperature = target

    def update(self, current_temperature: float) -> None:
        lower = self.target_temperature - self.hysteresis
        upper = self.target_temperature + self.hysteresis
        if current_temperature <= lower:
            self._heating_on = True
        elif current_temperature >= upper:
            self._heating_on = False

    def get_heating_command(self) -> float:
        return 1.0 if self._heating_on else 0.0
