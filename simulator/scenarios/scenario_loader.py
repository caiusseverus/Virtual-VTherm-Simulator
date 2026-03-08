"""Load scenarios from YAML."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from simulator.scenarios.scenario_schema import Scenario, scenario_from_dict


def _coerce_scalar(value: str):
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value.strip("\"'")


def _simple_yaml_parse(text: str) -> dict:
    """Very small YAML subset parser for nested mappings."""
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        key, _, value = line.partition(":")
        key = key.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]
        if value.strip() == "":
            new_dict: dict = {}
            current[key] = new_dict
            stack.append((indent, new_dict))
        else:
            current[key] = _coerce_scalar(value)
    return root


def _to_float(data: dict[str, Any], key: str, default: float) -> float:
    value = data.get(key, default)
    return float(value)


def _to_nested_schema(raw: dict[str, Any]) -> dict[str, Any]:
    if "simulation" in raw:
        simulation = dict(raw.get("simulation", {}))
        if "timestep_seconds" in simulation and "step_seconds" not in simulation:
            simulation["step_seconds"] = simulation["timestep_seconds"]

        weather = dict(raw.get("weather", {}))
        if "outdoor_temp" not in weather:
            weather["outdoor_temp"] = weather.get("outdoor_base_c", 5.0)

        return {
            "name": str(raw.get("name", "simulation")),
            "simulation": {
                "duration_hours": _to_float(simulation, "duration_hours", 24.0),
                "step_seconds": _to_float(simulation, "step_seconds", 60.0),
            },
            "building": {
                "initial_indoor_temp": _to_float(raw.get("building", {}), "initial_indoor_temp", 18.0),
                "thermal_mass": _to_float(raw.get("building", {}), "thermal_mass", 30_000_000.0),
                "heat_loss": _to_float(raw.get("building", {}), "heat_loss", 200.0),
            },
            "weather": {
                "outdoor_temp": _to_float(weather, "outdoor_temp", 5.0),
                "outdoor_base_c": _to_float(weather, "outdoor_base_c", weather.get("outdoor_temp", 5.0)),
                "outdoor_amplitude_c": _to_float(weather, "outdoor_amplitude_c", 0.0),
            },
            "heating": {"max_power_kw": _to_float(raw.get("heating", {}), "max_power_kw", 12.0)},
            "thermostat": {
                "target_temp": _to_float(raw.get("thermostat", {}), "target_temp", 21.0),
                "hysteresis": _to_float(raw.get("thermostat", {}), "hysteresis", 0.2),
                "mode": str(raw.get("thermostat", {}).get("mode", "mock_thermostat")),
                "integration_module_path": raw.get("thermostat", {}).get("integration_module_path"),
                "integration_revision": raw.get("thermostat", {}).get("integration_revision"),
            },
            "gains": {
                "solar_gain_kw": _to_float(raw.get("gains", {}), "solar_gain_kw", 0.0),
                "internal_heat_gain_kw": _to_float(raw.get("gains", {}), "internal_heat_gain_kw", 0.0),
            },
        }

    return {
        "name": str(raw.get("name", "simulation")),
        "simulation": {
            "duration_hours": _to_float(raw, "duration_hours", 24.0),
            "step_seconds": _to_float(raw, "step_seconds", 60.0),
        },
        "building": {
            "initial_indoor_temp": _to_float(raw, "indoor_initial_c", 18.0),
            "thermal_mass": _to_float(raw, "thermal_mass_j_per_c", _to_float(raw, "building_heat_capacity", 30_000_000.0)),
            "heat_loss": _to_float(raw, "heat_loss_w_per_c", _to_float(raw, "heat_loss_coefficient", 200.0)),
        },
        "weather": {
            "outdoor_temp": _to_float(raw, "outdoor_base_c", 5.0),
            "outdoor_base_c": _to_float(raw, "outdoor_base_c", 5.0),
            "outdoor_amplitude_c": _to_float(raw, "outdoor_amplitude_c", 0.0),
        },
        "heating": {
            "max_power_kw": _to_float(raw, "heating_power_kw", _to_float(raw, "max_heating_power_w", 12_000.0) / 1000.0)
        },
        "thermostat": {
            "target_temp": _to_float(raw, "target_temp_c", 21.0),
            "hysteresis": _to_float(raw, "hysteresis", 0.2),
            "mode": str(raw.get("thermostat_mode", "mock_thermostat")),
            "integration_module_path": raw.get("integration_module_path"),
            "integration_revision": raw.get("integration_revision"),
        },
        "gains": {
            "solar_gain_kw": _to_float(raw, "solar_gain_kw", 0.0),
            "internal_heat_gain_kw": _to_float(raw, "internal_heat_gain_kw", 0.0),
        },
    }


def load_scenario(path: str | Path) -> Scenario:
    """Load and validate a scenario YAML file."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        raw = yaml.safe_load(text)
    except Exception:
        raw = _simple_yaml_parse(text)
    normalized = _to_nested_schema(raw or {})
    return scenario_from_dict(normalized)
