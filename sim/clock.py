"""Simulation time helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SimulationClock:
    """Controllable simulation clock for deterministic, discrete stepping."""

    current: datetime

    def now(self) -> datetime:
        return self.current

    def advance(self, dt: timedelta) -> datetime:
        self.current += dt
        return self.current
