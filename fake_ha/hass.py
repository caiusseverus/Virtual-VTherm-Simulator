"""Composition root for fake Home Assistant components."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from sim.clock import SimulationClock

from .event_bus import EventBus
from .fake_services import FakeServices
from .scheduler import Scheduler
from .state_machine import StateMachine


@dataclass
class FakeHass:
    """Minimal Home Assistant-like runtime bundle."""

    initial_time: datetime
    states: StateMachine = field(default_factory=StateMachine)
    bus: EventBus = field(default_factory=EventBus)
    scheduler: Scheduler = field(default_factory=Scheduler)
    services: FakeServices = field(default_factory=FakeServices)
    config: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.time = SimulationClock(self.initial_time)
        self._register_default_services()

    def _register_default_services(self) -> None:
        def climate_turn_on(data: dict[str, Any]) -> None:
            entity_id = data.get("entity_id", "climate.virtual_thermostat")
            self.states.set(entity_id, "heat", {"hvac_mode": "heat"})

        def climate_turn_off(data: dict[str, Any]) -> None:
            entity_id = data.get("entity_id", "climate.virtual_thermostat")
            self.states.set(entity_id, "off", {"hvac_mode": "off"})

        def climate_set_temperature(data: dict[str, Any]) -> None:
            entity_id = data.get("entity_id", "climate.virtual_thermostat")
            temperature = float(data["temperature"])
            self.states.set(entity_id, "heat", {"temperature": temperature, "hvac_mode": "heat"})

        self.services.register("climate", "turn_on", climate_turn_on)
        self.services.register("climate", "turn_off", climate_turn_off)
        self.services.register("climate", "set_temperature", climate_set_temperature)
