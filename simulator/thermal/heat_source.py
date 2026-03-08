"""Heating source models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HeatSource:
    """Simple heat source with normalized command."""

    max_power_kw: float

    def output_power_w(self, command: float) -> float:
        command_clamped = max(0.0, min(1.0, command))
        return command_clamped * self.max_power_kw * 1000.0
