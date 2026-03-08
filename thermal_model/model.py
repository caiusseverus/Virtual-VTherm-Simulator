"""Adapted thermal model interface used by the simulation engine."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ThermalModel:
    """First-order building thermal model with optional gains."""

    building_heat_capacity: float
    heat_loss_coefficient: float
    heating_power_kw: float
    initial_indoor_temperature: float
    solar_gain_kw: float = 0.0
    internal_heat_gain_kw: float = 0.0

    def __post_init__(self) -> None:
        self._indoor_temperature = self.initial_indoor_temperature

    def step(self, heat_input_kw: float, outdoor_temp: float, dt: float) -> float:
        effective_heating_kw = max(0.0, min(heat_input_kw, self.heating_power_kw))
        heat_loss_kw = (self.heat_loss_coefficient * (self._indoor_temperature - outdoor_temp)) / 1000.0
        net_power_kw = effective_heating_kw + self.solar_gain_kw + self.internal_heat_gain_kw - heat_loss_kw
        delta_temp = (net_power_kw * 1000.0 * dt) / self.building_heat_capacity
        self._indoor_temperature += delta_temp
        return self._indoor_temperature

    def get_indoor_temperature(self) -> float:
        return self._indoor_temperature
