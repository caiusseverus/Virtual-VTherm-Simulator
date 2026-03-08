"""Simple in-memory state registry."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class State:
    """Container for entity state and attributes."""

    entity_id: str
    state: Any
    attributes: dict[str, Any] = field(default_factory=dict)
    last_changed: datetime = field(default_factory=datetime.utcnow)


class StateMachine:
    """A minimal subset of Home Assistant's state machine behavior."""

    def __init__(self) -> None:
        self._states: dict[str, State] = {}

    def set(self, entity_id: str, new_state: Any, attributes: dict[str, Any] | None = None) -> State:
        state = State(
            entity_id=entity_id,
            state=new_state,
            attributes=attributes or {},
            last_changed=datetime.utcnow(),
        )
        self._states[entity_id] = state
        return state

    def get(self, entity_id: str) -> State | None:
        return self._states.get(entity_id)

    def as_dict(self) -> dict[str, dict[str, Any]]:
        return {
            entity_id: {
                "state": state.state,
                "attributes": dict(state.attributes),
                "last_changed": state.last_changed.isoformat(),
            }
            for entity_id, state in self._states.items()
        }
