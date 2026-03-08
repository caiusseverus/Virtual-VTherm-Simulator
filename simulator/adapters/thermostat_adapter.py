"""Adapter around thermostat logic for offline simulation and HA-compat mode."""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any

from simulator.ha_stub import DEFAULT_CLIMATE_ENTITY_ID, HARuntime, register_climate_services


@dataclass
class _MockThermostatController:
    target_temperature: float
    hysteresis: float = 0.2
    heating_on: bool = False

    def set_temperature(self, target: float) -> None:
        self.target_temperature = target

    def compute_heating_command(self, *, current_temperature: float) -> float:
        lower = self.target_temperature - self.hysteresis
        upper = self.target_temperature + self.hysteresis
        if current_temperature <= lower:
            self.heating_on = True
        elif current_temperature >= upper:
            self.heating_on = False
        return 1.0 if self.heating_on else 0.0


@dataclass
class HACompatibilityWrapper:
    """Translate simulator data into expected integration payloads."""

    integration: Any

    def set_temperature(self, target: float) -> None:
        if hasattr(self.integration, "set_temperature"):
            self.integration.set_temperature(target)

    def compute_heating_command(self, payload: dict[str, Any]) -> float:
        if hasattr(self.integration, "compute_heating_command"):
            value = self.integration.compute_heating_command(payload)
        elif hasattr(self.integration, "update"):
            result = self.integration.update(payload)
            if result is not None:
                value = result
            elif hasattr(self.integration, "get_heating_command"):
                value = self.integration.get_heating_command()
            else:
                value = 0.0
        elif hasattr(self.integration, "get_heating_command"):
            value = self.integration.get_heating_command()
        else:
            raise TypeError("Integration does not expose a supported thermostat API")

        if isinstance(value, bool):
            return 1.0 if value else 0.0
        numeric = float(value)
        return max(0.0, min(1.0, numeric))


@dataclass
class ThermostatAdapter:
    """Thermostat adapter that supports mock and dynamic integration modes."""

    target_temperature: float
    hysteresis: float = 0.2
    mode: str = "mock_thermostat"
    integration_module_path: str | None = None
    integration_revision: str | None = None
    ha_runtime: HARuntime | None = None
    climate_entity_id: str = DEFAULT_CLIMATE_ENTITY_ID

    def __post_init__(self) -> None:
        self.ha = self.ha_runtime or HARuntime()
        self._setup_ha_compatibility()

        if self.mode == "mock_thermostat":
            self._controller: Any = _MockThermostatController(
                target_temperature=self.target_temperature,
                hysteresis=self.hysteresis,
            )
            self._compat = None
            return

        self._controller = self._load_dynamic_controller()
        self._compat = HACompatibilityWrapper(self._controller)

    def _setup_ha_compatibility(self) -> None:
        register_climate_services(
            self.ha,
            climate_entity_id=self.climate_entity_id,
            initial_temperature=self.target_temperature,
            source=self.mode,
        )

    def _load_dynamic_controller(self) -> Any:
        if not self.integration_module_path:
            raise ValueError("integration_module_path must be configured for dynamic adapter mode")

        module = self._load_module_from_path(self.integration_module_path, self.integration_revision)
        if hasattr(module, "build_thermostat"):
            return module.build_thermostat(
                target_temperature=self.target_temperature,
                hysteresis=self.hysteresis,
                revision=self.integration_revision,
            )
        if hasattr(module, "ThermostatIntegration"):
            cls = module.ThermostatIntegration
            return cls(
                target_temperature=self.target_temperature,
                hysteresis=self.hysteresis,
                revision=self.integration_revision,
            )
        raise AttributeError("Integration module must expose build_thermostat or ThermostatIntegration")

    @staticmethod
    def _load_module_from_path(module_path: str, revision: str | None) -> ModuleType:
        path = Path(module_path)
        if not path.exists():
            raise FileNotFoundError(f"Integration module not found: {module_path}")
        module_name = f"dynamic_thermostat_{path.stem}_{revision or 'default'}"
        spec = importlib.util.spec_from_file_location(module_name, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Unable to load module from {module_path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def set_temperature(self, target: float) -> None:
        self.ha.services.call(
            "climate",
            "set_temperature",
            {"entity_id": self.climate_entity_id, "temperature": target},
        )
        self.target_temperature = target
        if self.mode == "mock_thermostat":
            self._controller.set_temperature(target)
        elif self._compat is not None:
            self._compat.set_temperature(target)

    def update(self, current_temperature: float, *, outdoor_temperature: float | None = None, time_s: float = 0.0) -> None:
        climate_state = self.ha.states.get(self.climate_entity_id)
        target = float(climate_state.attributes.get("temperature", self.target_temperature)) if climate_state else self.target_temperature
        self.target_temperature = target

        self.ha.states.set("sensor.indoor_temperature", round(current_temperature, 3), {"unit": "°C"})
        if outdoor_temperature is not None:
            self.ha.states.set("sensor.outdoor_temperature", round(outdoor_temperature, 3), {"unit": "°C"})

        if self.mode == "mock_thermostat":
            self._controller.set_temperature(target)
            command = self._controller.compute_heating_command(current_temperature=current_temperature)
        else:
            payload = {
                "current_temperature": current_temperature,
                "target_temperature": target,
                "outdoor_temperature": outdoor_temperature,
                "time_s": time_s,
            }
            command = self._compat.compute_heating_command(payload)

        self.ha.states.set("sensor.heating_output", round(command, 3), {"unit": "ratio"})
        self.ha.services.call(
            "climate",
            "turn_on" if command > 0.0 else "turn_off",
            {
                "entity_id": self.climate_entity_id,
            },
        )

    def get_heating_command(self) -> float:
        heating_state = self.ha.states.get("sensor.heating_output")
        return float(heating_state.state) if heating_state is not None else 0.0
