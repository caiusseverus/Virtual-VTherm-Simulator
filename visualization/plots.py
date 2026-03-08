"""Graph generation helpers."""

from __future__ import annotations

import csv
from pathlib import Path


def _write_svg(rows: list[dict[str, float]], output: Path) -> Path:
    indoor = [row["indoor_temperature"] for row in rows]
    target = [row["target_temperature"] for row in rows]
    outdoor = [row["outdoor_temperature"] for row in rows]
    power = [row["heating_power_kw"] for row in rows]
    width, height, pad = 1000, 500, 40

    def scale(values: list[float]) -> list[float]:
        low, high = min(values), max(values)
        span = high - low or 1.0
        return [height - pad - ((v - low) / span) * (height - 2 * pad) for v in values]

    xs = [pad + i * (width - 2 * pad) / max(1, len(rows) - 1) for i in range(len(rows))]

    def polyline(ys: list[float], color: str) -> str:
        points = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
        return f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{points}"/>'

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        f'<rect width="{width}" height="{height}" fill="white"/>',
        polyline(scale(indoor), "#e74c3c"),
        polyline(scale(target), "#2ecc71"),
        polyline(scale(outdoor), "#3498db"),
        polyline(scale(power), "#f39c12"),
        "</svg>",
    ]
    output.write_text("\n".join(svg), encoding="utf-8")
    return output


def create_temperature_plot(csv_path: str, output_image: str | None = None) -> Path:
    rows: list[dict[str, float]] = []
    with open(csv_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append({
                "indoor_temperature": float(row["indoor_temperature"]),
                "target_temperature": float(row["target_temperature"]),
                "outdoor_temperature": float(row["outdoor_temperature"]),
                "heating_power_kw": float(row["heating_power_kw"]),
            })

    if not rows:
        raise ValueError("No data to plot")

    output = Path(output_image) if output_image else Path(csv_path).with_name("temperature.svg")
    output.parent.mkdir(parents=True, exist_ok=True)
    return _write_svg(rows, output)
