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
    outdoor_temp: float


@dataclass
class HeatingConfig:
    max_power_kw: float


@dataclass
class ThermostatConfig:
    target_temp: float
    hysteresis: float = 0.2


@dataclass
class Scenario:
    name: str
    simulation: SimulationConfig
    building: BuildingConfig
    weather: WeatherConfig
    heating: HeatingConfig
    thermostat: ThermostatConfig


def scenario_from_dict(raw: dict) -> Scenario:
    """Create a validated Scenario from mapping data."""
    return Scenario(
        name=str(raw["name"]),
        simulation=SimulationConfig(**raw["simulation"]),
        building=BuildingConfig(**raw["building"]),
        weather=WeatherConfig(**raw["weather"]),
        heating=HeatingConfig(**raw["heating"]),
        thermostat=ThermostatConfig(**raw["thermostat"]),
    )
