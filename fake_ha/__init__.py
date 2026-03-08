"""Minimal fake Home Assistant primitives for local simulation."""

from .hass import FakeHass
from .entity import Entity

__all__ = ["FakeHass", "Entity"]
