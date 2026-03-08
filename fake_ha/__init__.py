"""Minimal fake Home Assistant primitives for local simulation."""

from .entity import Entity
from .hass import FakeHass

__all__ = ["FakeHass", "Entity"]
