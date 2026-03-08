"""Main simulation engine orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import math
from typing import Any

from fake_ha.hass import FakeHass
from sim.scenario import SimulationScenario
from thermal_model.model import ThermalModel
from thermostat.adapter import ThermostatAdapter


@dataclass
class SimulationEngine:
    """Runs step-by-step thermal simulation for a scenario."""

    scenario: SimulationScenario

    def run(self) -> list[dict[str, Any]]:
        hass = FakeHass(initial_time=self.scenario.start_time)
        dt = timedelta(seconds=self.scenario.step_seconds)
        model = ThermalModel(
            building_heat_capacity=self.scenario.building_heat_capacity,
            heat_loss_coefficient=self.scenario.heat_loss_coefficient,
            heating_power_kw=self.scenario.heating_power_kw,
            initial_indoor_temperature=self.scenario.indoor_initial_c,
            solar_gain_kw=self.scenario.solar_gain_kw,
            internal_heat_gain_kw=self.scenario.internal_heat_gain_kw,
        )
        thermostat = ThermostatAdapter(max_power_kw=self.scenario.heating_power_kw)

        steps = int(self.scenario.duration.total_seconds() // self.scenario.step_seconds)
        rows: list[dict[str, Any]] = []

        for step in range(steps):
            now = hass.time.now()
            hour = now.hour + now.minute / 60.0
            outdoor_temp = self.scenario.outdoor_base_c + self.scenario.outdoor_amplitude_c * math.sin(
                2 * math.pi * (hour / 24.0)
            )

            thermostat.update(
                {
                    "indoor_temperature": model.get_indoor_temperature(),
                    "target_temperature": self.scenario.target_temp_c,
                    "time_of_day": hour,
                    "occupancy": True,
                    "external_temperature": outdoor_temp,
                }
            )
            heating_power_kw = thermostat.compute_heating_command()
            indoor_temp = model.step(heating_power_kw, outdoor_temp, self.scenario.step_seconds)

            hass.states.set("sensor.indoor_temperature", round(indoor_temp, 3), {"unit": "°C"})
            hass.states.set("sensor.outdoor_temperature", round(outdoor_temp, 3), {"unit": "°C"})
            hass.states.set("sensor.heating_power", round(heating_power_kw, 3), {"unit": "kW"})

            rows.append(
                {
                    "step": step,
                    "timestamp": now.isoformat(),
                    "indoor_temperature": indoor_temp,
                    "target_temperature": self.scenario.target_temp_c,
                    "heating_power_kw": heating_power_kw,
                    "outdoor_temperature": outdoor_temp,
                }
            )
            hass.time.advance(dt)

        return rows
