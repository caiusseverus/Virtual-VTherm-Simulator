"""Deprecated legacy sensor shims."""

from __future__ import annotations

import warnings

from simulator.thermal.weather_model import SinusoidalWeatherModel

warnings.warn(
    "sim.sensors is deprecated; use simulator.thermal.weather_model",
    DeprecationWarning,
    stacklevel=2,
)

OutdoorTempSensor = SinusoidalWeatherModel

__all__ = ["OutdoorTempSensor"]
