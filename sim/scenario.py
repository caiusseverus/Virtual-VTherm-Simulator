"""Deprecated legacy import shim for scenario loading."""

from __future__ import annotations

import warnings

from simulator.scenarios.scenario_loader import load_scenario
from simulator.scenarios.scenario_schema import Scenario

warnings.warn(
    "sim.scenario is deprecated; use simulator.scenarios",
    DeprecationWarning,
    stacklevel=2,
)

SimulationScenario = Scenario

__all__ = ["Scenario", "SimulationScenario", "load_scenario"]
