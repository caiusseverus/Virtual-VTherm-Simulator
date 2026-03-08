"""Main simulation loop."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from simulator.adapters.ha_runtime import HARuntime
from simulator.adapters.thermostat_adapter import ThermostatAdapter
from simulator.core.scheduler import Scheduler
from simulator.core.time_controller import TimeController
from simulator.metrics.metrics import MetricsRecorder
from simulator.scenarios.scenario_schema import Scenario
from simulator.thermal.building_model import BuildingModel
from simulator.thermal.heat_source import HeatSource
from simulator.thermal.weather_model import ConstantWeatherModel, SinusoidalWeatherModel


@dataclass
class SimulationResult:
    metrics: MetricsRecorder
    runtime_seconds: float
    simulated_seconds: float

    @property
    def speedup_factor(self) -> float:
        return self.simulated_seconds / self.runtime_seconds if self.runtime_seconds > 0 else float("inf")


class SimulationEngine:
    """Coordinates thermostat, heat source and building model."""

    def __init__(self, scenario: Scenario) -> None:
        self.scenario = scenario
        self.clock = TimeController(0.0)
        self.scheduler = Scheduler()
        self.metrics = MetricsRecorder()
        self.ha = HARuntime()

        self.thermostat = ThermostatAdapter(
            target_temperature=scenario.thermostat.target_temp,
            hysteresis=scenario.thermostat.hysteresis,
        )
        self.building = BuildingModel(
            indoor_temperature=scenario.building.initial_indoor_temp,
            thermal_mass=scenario.building.thermal_mass,
            heat_loss_coefficient=scenario.building.heat_loss,
        )
        self.heat_source = HeatSource(max_power_kw=scenario.heating.max_power_kw)
        if scenario.weather.outdoor_amplitude_c != 0.0:
            self.weather = SinusoidalWeatherModel(
                base_c=scenario.weather.outdoor_base_c,
                amplitude_c=scenario.weather.outdoor_amplitude_c,
            )
        else:
            self.weather = ConstantWeatherModel(outdoor_temp=scenario.weather.outdoor_temp)

    def run(self) -> SimulationResult:
        step_s = self.scenario.simulation.step_seconds
        total_s = self.scenario.simulation.duration_hours * 3600.0
        steps = int(total_s / step_s)

        start = perf_counter()
        cumulative_energy_kwh = 0.0

        solar_gain_w = self.scenario.gains.solar_gain_kw * 1000.0
        internal_gain_w = self.scenario.gains.internal_heat_gain_kw * 1000.0

        for _ in range(steps):
            now_s = self.clock.current_time_s
            outdoor = self.weather.get_temperature(now_s)

            self.scheduler.run_due(now_s)
            self.thermostat.update(self.building.indoor_temperature)
            heating_command = self.thermostat.get_heating_command()
            power_w = self.heat_source.output_power_w(heating_command)
            indoor = self.building.step(step_s, outdoor, power_w, solar_gain_w, internal_gain_w)

            cumulative_energy_kwh += power_w * (step_s / 3600.0) / 1000.0
            self.ha.states.set("sensor.indoor_temperature", round(indoor, 3), {"unit": "°C"})
            self.ha.states.set("sensor.outdoor_temperature", round(outdoor, 3), {"unit": "°C"})
            self.ha.states.set("sensor.heating_output", round(heating_command, 3), {"unit": "ratio"})

            self.metrics.record(
                time_s=now_s,
                indoor_temperature=indoor,
                outdoor_temperature=outdoor,
                target_temperature=self.thermostat.target_temperature,
                heating_output=heating_command,
                energy_consumption_kwh=cumulative_energy_kwh,
            )
            self.clock.advance(step_s)

        runtime = perf_counter() - start
        return SimulationResult(self.metrics, runtime, total_s)
