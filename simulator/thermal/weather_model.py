"""Weather model utilities."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class ConstantWeatherModel:
    """Constant outdoor temperature model."""

    outdoor_temp: float

    def get_temperature(self, _time_s: float) -> float:
        return self.outdoor_temp


@dataclass
class SinusoidalWeatherModel:
    """Sinusoidal outdoor temperature model over a 24h period."""

    base_c: float
    amplitude_c: float

    def get_temperature(self, time_s: float) -> float:
        phase = 2.0 * math.pi * ((time_s % 86400.0) / 86400.0)
        return self.base_c + self.amplitude_c * math.sin(phase - math.pi / 2.0)
