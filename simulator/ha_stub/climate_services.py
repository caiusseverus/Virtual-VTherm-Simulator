"""Minimal climate service handlers for simulator runtime."""

from __future__ import annotations

from typing import Any

from simulator.ha_stub.runtime import HARuntime


DEFAULT_CLIMATE_ENTITY_ID = "climate.simulated_thermostat"


def register_climate_services(
    runtime: HARuntime,
    *,
    climate_entity_id: str = DEFAULT_CLIMATE_ENTITY_ID,
    initial_temperature: float = 20.0,
    source: str = "simulator",
) -> None:
    runtime.states.set(
        climate_entity_id,
        "off",
        {
            "temperature": initial_temperature,
            "hvac_mode": "off",
            "source": source,
        },
    )

    def set_temperature(data: dict[str, Any]) -> None:
        entity_id = data.get("entity_id", climate_entity_id)
        state = runtime.states.get(entity_id)
        if state is None:
            return
        attrs = dict(state.attributes)
        attrs["temperature"] = float(data["temperature"])
        runtime.states.set(entity_id, state.state, attrs)

    def turn_on(data: dict[str, Any]) -> None:
        _set_hvac_mode(runtime, data.get("entity_id", climate_entity_id), "heat")

    def turn_off(data: dict[str, Any]) -> None:
        _set_hvac_mode(runtime, data.get("entity_id", climate_entity_id), "off")

    runtime.services.register("climate", "set_temperature", set_temperature)
    runtime.services.register("climate", "turn_on", turn_on)
    runtime.services.register("climate", "turn_off", turn_off)


def _set_hvac_mode(runtime: HARuntime, entity_id: str, hvac_mode: str) -> None:
    state = runtime.states.get(entity_id)
    if state is None:
        return
    attrs = dict(state.attributes)
    attrs["hvac_mode"] = hvac_mode
    runtime.states.set(entity_id, hvac_mode, attrs)
