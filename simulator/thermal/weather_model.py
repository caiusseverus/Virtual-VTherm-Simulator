"""Weather model utilities."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ConstantWeatherModel:
    """Constant outdoor temperature model."""

    outdoor_temp: float

    def get_temperature(self, _time_s: float) -> float:
        return self.outdoor_temp
