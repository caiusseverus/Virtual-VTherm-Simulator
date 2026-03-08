"""Minimal Home Assistant-like entities used by the simulator."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class Entity:
    entity_id: str
    state: Any = None
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SensorEntity(Entity):
    pass


@dataclass
class SwitchEntity(Entity):
    pass


@dataclass
class ClimateEntity(Entity):
    target_temperature: float = 20.0
