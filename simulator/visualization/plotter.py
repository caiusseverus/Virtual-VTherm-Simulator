"""Plot simulation outputs."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def generate_plots(df: Any, output_dir: str | Path) -> dict[str, Path]:
    """Generate required plots and return file paths."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    try:
        import matplotlib.pyplot as plt  # type: ignore
    except Exception:
        placeholders = {
            "temperature_vs_target": out / "temperature_vs_target.png",
            "heating_output": out / "heating_output.png",
            "energy_usage": out / "energy_usage.png",
        }
        for p in placeholders.values():
            p.write_text("matplotlib not installed", encoding="utf-8")
        return placeholders

    time_h = [t / 3600.0 for t in df["time_s"]]

    files: dict[str, Path] = {}

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(time_h, df["indoor_temperature"], label="Indoor")
    ax.plot(time_h, df["target_temperature"], label="Target", linestyle="--")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    temp_path = out / "temperature_vs_target.png"
    fig.tight_layout()
    fig.savefig(temp_path)
    plt.close(fig)
    files["temperature_vs_target"] = temp_path

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(time_h, df["heating_output"], color="tab:red")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Heating output (0-1)")
    heat_path = out / "heating_output.png"
    fig.tight_layout()
    fig.savefig(heat_path)
    plt.close(fig)
    files["heating_output"] = heat_path

    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(time_h, df["energy_consumption"], color="tab:green")
    ax.set_xlabel("Time (h)")
    ax.set_ylabel("Cumulative energy (kWh)")
    energy_path = out / "energy_usage.png"
    fig.tight_layout()
    fig.savefig(energy_path)
    plt.close(fig)
    files["energy_usage"] = energy_path

    return files
