"""Simulation clock helper."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class SimulationClock:
    """Discrete clock used by the engine."""

    current: datetime
    step: timedelta

    def tick(self) -> datetime:
        self.current += self.step
        return self.current
