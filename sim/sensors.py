"""Virtual sensors for generating environment signals."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import datetime


@dataclass
class OutdoorTempSensor:
    """A simple sinusoidal daily outdoor temperature profile."""

    base_c: float
    amplitude_c: float

    def read(self, timestamp: datetime) -> float:
        seconds_since_midnight = timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second
        phase = 2.0 * math.pi * seconds_since_midnight / 86400.0
        return self.base_c + self.amplitude_c * math.sin(phase - math.pi / 2.0)
