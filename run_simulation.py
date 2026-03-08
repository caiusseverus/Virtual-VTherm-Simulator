"""CLI runner for thermostat simulations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from simulator.core.simulation_engine import SimulationEngine
from simulator.scenarios.scenario_loader import load_scenario
from simulator.visualization.plotter import generate_plots


def main() -> None:
    parser = argparse.ArgumentParser(description="Run thermostat simulation")
    parser.add_argument("scenario", help="Path to YAML scenario")
    parser.add_argument("--output", default="simulator/results/cli_run", help="Output directory")
    args = parser.parse_args()

    scenario = load_scenario(args.scenario)
    engine = SimulationEngine(scenario)
    result = engine.run()

    output_dir = Path(args.output)
    csv_path = result.metrics.save_csv(output_dir / "metrics.csv")
    plot_paths = generate_plots(result.metrics.to_dataframe(), output_dir)
    summary = result.metrics.summarize(scenario.simulation.step_seconds)
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary.__dict__, indent=2), encoding="utf-8")

    print(f"Scenario: {scenario.name}")
    print(f"Runtime: {result.runtime_seconds:.4f}s")
    print(f"Simulated: {result.simulated_seconds/3600:.1f}h")
    print(f"Speedup: {result.speedup_factor:.1f}x")
    print(f"CSV: {csv_path}")
    print(f"Summary: {summary_path}")
    for name, path in plot_paths.items():
        print(f"{name}: {path}")


if __name__ == "__main__":
    main()
