"""FastAPI endpoints for running simulations."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from simulator.core.simulation_engine import SimulationEngine
from simulator.scenarios.scenario_schema import Scenario
from simulator.visualization.plotter import generate_plots

router = APIRouter()
RESULTS_DIR = Path("simulator/results")
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


class SimulateRequest(BaseModel):
    scenario: Scenario


@router.get("/scenarios")
def list_scenarios() -> list[str]:
    return sorted(p.name for p in Path("scenarios").glob("*.yaml"))


@router.post("/simulate")
def simulate(req: SimulateRequest) -> dict[str, str | float]:
    engine = SimulationEngine(req.scenario)
    result = engine.run()
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    run_dir = RESULTS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    csv_path = result.metrics.save_csv(run_dir / "metrics.csv")
    plots = generate_plots(result.metrics.to_dataframe(), run_dir)

    return {
        "id": run_id,
        "csv": str(csv_path),
        "temperature_plot": str(plots["temperature_vs_target"]),
        "heating_plot": str(plots["heating_output"]),
        "energy_plot": str(plots["energy_usage"]),
        "runtime_seconds": result.runtime_seconds,
        "speedup_factor": result.speedup_factor,
    }


@router.get("/results/{run_id}")
def get_results(run_id: str) -> dict[str, str]:
    run_dir = RESULTS_DIR / run_id
    if not run_dir.exists():
        raise HTTPException(status_code=404, detail="Result not found")
    return {
        "csv": str(run_dir / "metrics.csv"),
        "temperature_plot": str(run_dir / "temperature_vs_target.png"),
        "heating_plot": str(run_dir / "heating_output.png"),
        "energy_plot": str(run_dir / "energy_usage.png"),
    }
