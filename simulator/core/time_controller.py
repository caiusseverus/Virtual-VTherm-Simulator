"""Deterministic virtual time controller."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TimeController:
    """Keeps simulation time in seconds."""

    current_time_s: float = 0.0

    def advance(self, step_seconds: float) -> float:
        """Advance the simulation clock."""
        self.current_time_s += step_seconds
        return self.current_time_s
