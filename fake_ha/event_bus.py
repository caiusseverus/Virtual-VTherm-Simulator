"""Simple publish/subscribe event bus."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Callable


@dataclass(slots=True)
class Event:
    """Recorded event object."""

    event_type: str
    data: dict[str, Any] = field(default_factory=dict)
    time_fired: datetime = field(default_factory=datetime.utcnow)


class EventBus:
    """A tiny callback-based event bus."""

    def __init__(self) -> None:
        self._listeners: dict[str, list[Callable[[Event], None]]] = defaultdict(list)

    def listen(self, event_type: str, callback: Callable[[Event], None]) -> None:
        self._listeners[event_type].append(callback)

    def fire(self, event_type: str, data: dict[str, Any] | None = None) -> Event:
        event = Event(event_type=event_type, data=data or {})
        for callback in self._listeners.get(event_type, []):
            callback(event)
        return event
