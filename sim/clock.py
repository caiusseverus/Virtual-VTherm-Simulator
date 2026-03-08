"""Deprecated legacy clock shim."""

from __future__ import annotations

import warnings

from simulator.core.time_controller import TimeController

warnings.warn(
    "sim.clock is deprecated; use simulator.core.time_controller",
    DeprecationWarning,
    stacklevel=2,
)

SimulationClock = TimeController

__all__ = ["SimulationClock"]
