"""Minimal service registry and climate service handlers."""

from __future__ import annotations

from typing import Any, Callable


class FakeServices:
    """Very small subset of Home Assistant service registry."""

    def __init__(self) -> None:
        self._handlers: dict[tuple[str, str], Callable[[dict[str, Any]], Any]] = {}

    def register(self, domain: str, service: str, handler: Callable[[dict[str, Any]], Any]) -> None:
        self._handlers[(domain, service)] = handler

    def call(self, domain: str, service: str, data: dict[str, Any] | None = None) -> Any:
        key = (domain, service)
        if key not in self._handlers:
            raise KeyError(f"Service {domain}.{service} not found")
        return self._handlers[key](data or {})
