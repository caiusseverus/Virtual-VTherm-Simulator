"""Helpers emulating a versatile thermostat config loader."""

from __future__ import annotations

from typing import Any


def _parse_simple_yaml(path: str) -> dict[str, Any]:
    out: dict[str, Any] = {}
    with open(path, "r", encoding="utf-8") as file:
        for raw in file:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            key, sep, value = line.partition(":")
            if not sep:
                continue
            cleaned = value.strip().strip('"').strip("'")
            try:
                casted: Any = float(cleaned) if "." in cleaned else int(cleaned)
            except ValueError:
                casted = cleaned
            out[key.strip()] = casted
    return out


def load_versatile_config(path: str) -> dict[str, Any]:
    """Load and lightly validate YAML-like config used by integration adapters."""
    config = _parse_simple_yaml(path)

    if not isinstance(config, dict):
        raise ValueError("Config file must contain a mapping object.")

    required = {"name", "target_temp_c", "max_heating_power_w"}
    missing = required.difference(config)
    if missing:
        raise ValueError(f"Missing required keys: {sorted(missing)}")

    return config
