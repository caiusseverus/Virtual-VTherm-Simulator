"""Deprecated legacy import shim for SimulationEngine."""

from __future__ import annotations

import warnings

from simulator.core.simulation_engine import SimulationEngine, SimulationResult

warnings.warn(
    "sim.engine is deprecated; use simulator.core.simulation_engine",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["SimulationEngine", "SimulationResult"]
