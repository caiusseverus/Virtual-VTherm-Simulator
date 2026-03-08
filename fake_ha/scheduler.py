"""Deterministic scheduler for simulation callbacks."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Callable


@dataclass(order=True, slots=True)
class ScheduledTask:
    """A callback to execute at a specific timestamp."""

    run_at: datetime
    callback: Callable[[], None] = field(compare=False)
    name: str = field(default="task", compare=False)


class Scheduler:
    """Priority-queue-based scheduler."""

    def __init__(self) -> None:
        self._queue: list[ScheduledTask] = []

    def call_at(self, run_at: datetime, callback: Callable[[], None], name: str = "task") -> None:
        heapq.heappush(self._queue, ScheduledTask(run_at=run_at, callback=callback, name=name))

    def call_later(self, now: datetime, delay: timedelta, callback: Callable[[], None], name: str = "task") -> None:
        self.call_at(now + delay, callback, name=name)

    def run_due(self, now: datetime) -> int:
        count = 0
        while self._queue and self._queue[0].run_at <= now:
            task = heapq.heappop(self._queue)
            task.callback()
            count += 1
        return count
