"""Main simulation engine orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from typing import Any

from fake_ha.hass import FakeHass
from models.building_model import BuildingModel
from models.heating_plant import HeatingPlant
from sim.clock import SimulationClock
from sim.scenario import SimulationScenario
from sim.sensors import OutdoorTempSensor


@dataclass
class SimulationEngine:
    """Runs step-by-step thermal simulation for a scenario."""

    scenario: SimulationScenario

    def run(self) -> list[dict[str, Any]]:
        hass = FakeHass()
        clock = SimulationClock(self.scenario.start_time, timedelta(seconds=self.scenario.step_seconds))
        building = BuildingModel(
            initial_indoor_temp_c=self.scenario.indoor_initial_c,
            thermal_mass_j_per_c=self.scenario.thermal_mass_j_per_c,
            heat_loss_w_per_c=self.scenario.heat_loss_w_per_c,
        )
        plant = HeatingPlant(max_power_w=self.scenario.max_heating_power_w)
        outdoor = OutdoorTempSensor(base_c=self.scenario.outdoor_base_c, amplitude_c=self.scenario.outdoor_amplitude_c)

        steps = int(self.scenario.duration.total_seconds() // self.scenario.step_seconds)
        indoor_temp = building.initial_indoor_temp_c
        rows: list[dict[str, Any]] = []

        for _ in range(steps):
            now = clock.current
            outdoor_temp = outdoor.read(now)
            error = self.scenario.target_temp_c - indoor_temp
            demand = max(0.0, min(1.0, error / 3.0))
            heating_power = plant.output_power(demand)

            indoor_temp = building.step(
                indoor_temp_c=indoor_temp,
                outdoor_temp_c=outdoor_temp,
                hvac_power_w=heating_power,
                dt_seconds=self.scenario.step_seconds,
            )

            hass.states.set("sensor.indoor_temperature", round(indoor_temp, 3), {"unit": "°C"})
            hass.states.set("sensor.outdoor_temperature", round(outdoor_temp, 3), {"unit": "°C"})
            hass.states.set("sensor.heating_power", round(heating_power, 1), {"unit": "W"})

            rows.append(
                {
                    "timestamp": now.isoformat(),
                    "indoor_temp_c": indoor_temp,
                    "outdoor_temp_c": outdoor_temp,
                    "target_temp_c": self.scenario.target_temp_c,
                    "heating_power_w": heating_power,
                    "demand": demand,
                }
            )
            clock.tick()

        return rows
