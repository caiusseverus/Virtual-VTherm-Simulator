"""First-order building thermal model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BuildingModel:
    """Represents indoor thermal mass and heat exchange with outdoors."""

    initial_indoor_temp_c: float
    thermal_mass_j_per_c: float
    heat_loss_w_per_c: float

    def step(self, indoor_temp_c: float, outdoor_temp_c: float, hvac_power_w: float, dt_seconds: float) -> float:
        temp_diff = indoor_temp_c - outdoor_temp_c
        net_power_w = hvac_power_w - self.heat_loss_w_per_c * temp_diff
        delta_temp = (net_power_w * dt_seconds) / self.thermal_mass_j_per_c
        return indoor_temp_c + delta_temp
