"""CLI entrypoint for running thermal simulation scenarios."""

from __future__ import annotations

import argparse

from analysis.recorder import Recorder
from sim.engine import SimulationEngine
from sim.scenario import SimulationScenario


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a virtual thermal simulation scenario.")
    parser.add_argument("--scenario", required=True, help="Path to scenario YAML file.")
    parser.add_argument("--output", default="output/simulation.csv", help="CSV output path.")
    parser.add_argument("--plot", action="store_true", help="Generate a PNG plot next to output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    scenario = SimulationScenario.from_yaml(args.scenario)
    engine = SimulationEngine(scenario)
    rows = engine.run()

    recorder = Recorder()
    csv_path = recorder.write_csv(rows, args.output)
    print(f"Wrote {len(rows)} rows to {csv_path}")

    if args.plot:
        from analysis.graphs import plot_run

        image_path = plot_run(str(csv_path))
        print(f"Wrote plot to {image_path}")


if __name__ == "__main__":
    main()
