"""Plot-like rendering helper for simulation outputs (pure stdlib SVG)."""

from __future__ import annotations

import csv
from pathlib import Path


def _scale(values: list[float], min_px: float, max_px: float) -> list[float]:
    low = min(values)
    high = max(values)
    span = high - low or 1.0
    return [max_px - ((v - low) / span) * (max_px - min_px) for v in values]


def _polyline(xs: list[float], ys: list[float], color: str) -> str:
    points = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    return f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{points}" />'


def plot_run(csv_path: str, output_image: str | None = None) -> Path:
    """Generate a simple SVG plot of temperatures and heating power."""
    indoor: list[float] = []
    outdoor: list[float] = []
    target: list[float] = []
    power: list[float] = []

    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            indoor.append(float(row["indoor_temp_c"]))
            outdoor.append(float(row["outdoor_temp_c"]))
            target.append(float(row["target_temp_c"]))
            power.append(float(row["heating_power_w"]))

    if not indoor:
        raise ValueError("CSV file has no rows to plot.")

    width, height = 1000, 500
    pad = 40
    xs = [pad + i * (width - 2 * pad) / max(1, (len(indoor) - 1)) for i in range(len(indoor))]

    temp_ys_indoor = _scale(indoor, pad, height - pad)
    temp_ys_outdoor = _scale(outdoor, pad, height - pad)
    temp_ys_target = _scale(target, pad, height - pad)
    power_ys = _scale(power, pad, height - pad)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        f'<line x1="{pad}" y1="{height-pad}" x2="{width-pad}" y2="{height-pad}" stroke="#777"/>',
        f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{height-pad}" stroke="#777"/>',
        _polyline(xs, temp_ys_indoor, "#e74c3c"),
        _polyline(xs, temp_ys_outdoor, "#3498db"),
        _polyline(xs, temp_ys_target, "#2ecc71"),
        _polyline(xs, power_ys, "#f39c12"),
        '<text x="50" y="20" font-size="14" fill="#222">Indoor (red), Outdoor (blue), Target (green), Power (orange)</text>',
        '</svg>',
    ]

    out = Path(output_image) if output_image else Path(csv_path).with_suffix(".svg")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(svg), encoding="utf-8")
    return out
