"""CLI entrypoint for running thermal simulation scenarios."""

from __future__ import annotations

import argparse
import json

from analysis.recorder import Recorder
from sim.engine import SimulationEngine
from sim.metrics import summarize
from sim.scenario import SimulationScenario
from visualization.plots import create_temperature_plot


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a virtual thermal simulation scenario.")
    parser.add_argument("--scenario", required=True, help="Path to scenario YAML file.")
    parser.add_argument("--output", default="results/run_001/simulation.csv", help="CSV output path.")
    parser.add_argument("--plot", action="store_true", help="Generate a plot next to output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenario = SimulationScenario.from_yaml(args.scenario)
    rows = SimulationEngine(scenario).run()

    recorder = Recorder()
    csv_path = recorder.write_csv(rows, args.output)
    metrics = summarize(rows, scenario.step_seconds)

    metrics_path = csv_path.with_name("metrics.json")
    metrics_path.write_text(json.dumps(metrics.__dict__, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} rows to {csv_path}")
    print(f"Wrote metrics to {metrics_path}")

    if args.plot:
        image_path = create_temperature_plot(str(csv_path))
        print(f"Wrote plot to {image_path}")


if __name__ == "__main__":
    main()
