"""Scenario schema definitions."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SimulationConfig:
    duration_hours: float
    step_seconds: float


@dataclass
class BuildingConfig:
    thermal_mass: float
    heat_loss: float
    initial_indoor_temp: float = 18.0


@dataclass
class WeatherConfig:
    outdoor_temp: float = 5.0
    outdoor_base_c: float = 5.0
    outdoor_amplitude_c: float = 0.0


@dataclass
class HeatingConfig:
    max_power_kw: float


@dataclass
class ThermostatConfig:
    target_temp: float
    hysteresis: float = 0.2
    mode: str = "mock_thermostat"
    integration_module_path: str | None = None
    integration_revision: str | None = None


@dataclass
class GainsConfig:
    solar_gain_kw: float = 0.0
    internal_heat_gain_kw: float = 0.0


@dataclass
class Scenario:
    name: str
    simulation: SimulationConfig
    building: BuildingConfig
    weather: WeatherConfig
    heating: HeatingConfig
    thermostat: ThermostatConfig
    gains: GainsConfig


def scenario_from_dict(raw: dict) -> Scenario:
    """Create a validated Scenario from mapping data."""
    return Scenario(
        name=str(raw["name"]),
        simulation=SimulationConfig(**raw["simulation"]),
        building=BuildingConfig(**raw["building"]),
        weather=WeatherConfig(**raw["weather"]),
        heating=HeatingConfig(**raw["heating"]),
        thermostat=ThermostatConfig(**raw["thermostat"]),
        gains=GainsConfig(**raw.get("gains", {})),
    )
