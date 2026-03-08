"""Load scenarios from YAML."""

from __future__ import annotations

from pathlib import Path

from simulator.scenarios.scenario_schema import Scenario, scenario_from_dict


def _coerce_scalar(value: str):
    value = value.strip()
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value.strip("\"'")


def _simple_yaml_parse(text: str) -> dict:
    """Very small YAML subset parser for nested mappings."""
    root: dict = {}
    stack: list[tuple[int, dict]] = [(-1, root)]
    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.strip().startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        key, _, value = line.partition(":")
        key = key.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]
        if value.strip() == "":
            new_dict: dict = {}
            current[key] = new_dict
            stack.append((indent, new_dict))
        else:
            current[key] = _coerce_scalar(value)
    return root


def load_scenario(path: str | Path) -> Scenario:
    """Load and validate a scenario YAML file."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore

        raw = yaml.safe_load(text)
    except Exception:
        raw = _simple_yaml_parse(text)
    return scenario_from_dict(raw)
