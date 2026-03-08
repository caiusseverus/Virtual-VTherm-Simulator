"""Composition root for fake Home Assistant components."""

from __future__ import annotations

from dataclasses import dataclass, field

from .event_bus import EventBus
from .scheduler import Scheduler
from .state_machine import StateMachine


@dataclass
class FakeHass:
    """Minimal Home Assistant-like runtime bundle."""

    states: StateMachine = field(default_factory=StateMachine)
    bus: EventBus = field(default_factory=EventBus)
    scheduler: Scheduler = field(default_factory=Scheduler)
