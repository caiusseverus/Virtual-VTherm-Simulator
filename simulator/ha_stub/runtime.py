"""Home Assistant-like runtime primitives for deterministic simulation."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable


@dataclass(slots=True)
class HAState:
    entity_id: str
    state: Any
    attributes: dict[str, Any] = field(default_factory=dict)
    last_changed: datetime = field(default_factory=datetime.utcnow)


class HAStateMachine:
    def __init__(self, now: Callable[[], datetime] | None = None) -> None:
        self._states: dict[str, HAState] = {}
        self._now = now or datetime.utcnow

    def set(self, entity_id: str, state: Any, attributes: dict[str, Any] | None = None) -> HAState:
        ha_state = HAState(
            entity_id=entity_id,
            state=state,
            attributes=attributes or {},
            last_changed=self._now(),
        )
        self._states[entity_id] = ha_state
        return ha_state

    def get(self, entity_id: str) -> HAState | None:
        return self._states.get(entity_id)


@dataclass(slots=True)
class HAEvent:
    event_type: str
    data: dict[str, Any] = field(default_factory=dict)
    time_fired: datetime = field(default_factory=datetime.utcnow)


class HAEventBus:
    def __init__(self, now: Callable[[], datetime] | None = None) -> None:
        self._listeners: dict[str, list[Callable[[HAEvent], None]]] = defaultdict(list)
        self._now = now or datetime.utcnow

    def listen(self, event_type: str, callback: Callable[[HAEvent], None]) -> None:
        self._listeners[event_type].append(callback)

    def fire(self, event_type: str, data: dict[str, Any] | None = None) -> HAEvent:
        event = HAEvent(event_type=event_type, data=data or {}, time_fired=self._now())
        for callback in self._listeners.get(event_type, []):
            callback(event)
        return event


class HAServiceRegistry:
    def __init__(self) -> None:
        self._handlers: dict[tuple[str, str], Callable[[dict[str, Any]], Any]] = {}

    def register(self, domain: str, service: str, handler: Callable[[dict[str, Any]], Any]) -> None:
        self._handlers[(domain, service)] = handler

    def call(self, domain: str, service: str, data: dict[str, Any] | None = None) -> Any:
        key = (domain, service)
        if key not in self._handlers:
            raise KeyError(f"Service {domain}.{service} not found")
        return self._handlers[key](data or {})


@dataclass
class HARuntime:
    """Composable HA-like runtime used by the simulator stack."""

    now: Callable[[], datetime] = datetime.utcnow
    states: HAStateMachine = field(init=False)
    bus: HAEventBus = field(init=False)
    services: HAServiceRegistry = field(default_factory=HAServiceRegistry)

    def __post_init__(self) -> None:
        self.states = HAStateMachine(now=self.now)
        self.bus = HAEventBus(now=self.now)
