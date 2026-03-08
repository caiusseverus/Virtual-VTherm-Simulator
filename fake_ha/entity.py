"""Base fake entity implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entity:
    """Base entity that can publish itself into FakeHass state machine."""

    entity_id: str
    name: str
    state: Any = None
    attributes: dict[str, Any] = field(default_factory=dict)

    def set_state(self, value: Any, **attributes: Any) -> None:
        self.state = value
        self.attributes.update(attributes)

    def write_state(self, hass: "FakeHass") -> None:
        hass.states.set(self.entity_id, self.state, dict(self.attributes))
