"""Deterministic event scheduler."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from typing import Callable, List


Callback = Callable[[float], None]


@dataclass(order=True)
class ScheduledTask:
    run_at: float
    interval: float | None = field(compare=False, default=None)
    callback: Callback = field(compare=False, default=lambda _: None)


class Scheduler:
    """Simple scheduler inspired by Home Assistant timers."""

    def __init__(self) -> None:
        self._queue: List[ScheduledTask] = []

    def schedule_later(self, now_s: float, delay_s: float, callback: Callback) -> None:
        heapq.heappush(self._queue, ScheduledTask(run_at=now_s + delay_s, callback=callback))

    def schedule_interval(self, now_s: float, interval_s: float, callback: Callback) -> None:
        heapq.heappush(
            self._queue,
            ScheduledTask(run_at=now_s + interval_s, interval=interval_s, callback=callback),
        )

    def run_due(self, now_s: float) -> None:
        while self._queue and self._queue[0].run_at <= now_s:
            task = heapq.heappop(self._queue)
            task.callback(now_s)
            if task.interval is not None:
                task.run_at = now_s + task.interval
                heapq.heappush(self._queue, task)
