"""Simple heater plant with modulation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HeatingPlant:
    """Converts thermostat demand ratio to output power."""

    max_power_w: float
    efficiency: float = 1.0

    def output_power(self, demand_ratio: float) -> float:
        demand = max(0.0, min(1.0, demand_ratio))
        return self.max_power_w * demand * self.efficiency
