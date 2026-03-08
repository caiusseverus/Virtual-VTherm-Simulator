"""Thermal building model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BuildingModel:
    """Single-node thermal model.

    dT/dt = (heating_power_w + gains_w - heat_loss_coefficient * (Tin - Tout)) / thermal_mass
    where thermal_mass in J/K and heat_loss_coefficient in W/K.
    """

    indoor_temperature: float
    thermal_mass: float
    heat_loss_coefficient: float

    def step(
        self,
        dt_s: float,
        outdoor_temperature: float,
        heating_power_w: float,
        solar_gain_w: float = 0.0,
        internal_gain_w: float = 0.0,
    ) -> float:
        heat_loss = self.heat_loss_coefficient * (self.indoor_temperature - outdoor_temperature)
        total_input_power = heating_power_w + solar_gain_w + internal_gain_w
        dtemp = (total_input_power - heat_loss) / self.thermal_mass * dt_s
        self.indoor_temperature += dtemp
        return self.indoor_temperature
