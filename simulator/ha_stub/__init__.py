"""Canonical Home Assistant stubs used by simulator components."""

from simulator.ha_stub.climate_services import DEFAULT_CLIMATE_ENTITY_ID, register_climate_services
from simulator.ha_stub.runtime import HARuntime, HAEvent, HAEventBus, HAServiceRegistry, HAState, HAStateMachine

__all__ = [
    "DEFAULT_CLIMATE_ENTITY_ID",
    "register_climate_services",
    "HARuntime",
    "HAState",
    "HAStateMachine",
    "HAEvent",
    "HAEventBus",
    "HAServiceRegistry",
]
