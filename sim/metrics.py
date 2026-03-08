"""Deprecated legacy import shim for metrics summaries."""

from __future__ import annotations

import warnings

from simulator.metrics.metrics import MetricsSummary, summarize

warnings.warn(
    "sim.metrics is deprecated; use simulator.metrics.metrics",
    DeprecationWarning,
    stacklevel=2,
)

__all__ = ["MetricsSummary", "summarize"]
