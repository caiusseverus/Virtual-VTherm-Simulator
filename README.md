# Thermostat Offline Simulator

Fast offline simulation framework for testing thermostat control algorithms against a thermal building model without Home Assistant runtime.

## Features
- Deterministic virtual-time simulation loop (no sleeps)
- Thermal building model + heat source + thermostat adapter
- YAML-driven scenarios
- CSV metrics and PNG graphs
- FastAPI web UI to run simulations interactively
- Pytest coverage for core pieces

## Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## CLI usage
```bash
python run_simulation.py scenarios/winter_test.yaml
```

## Web UI
```bash
python -m uvicorn simulator.web.server:app --reload
```
Open http://localhost:8000

## API
- `GET /scenarios`
- `POST /simulate`
- `GET /results/{id}`

## Performance target
Default scenario (`48h`, `10s` step) is designed to run far faster than real-time (typically >100x speedup on modern CPUs).
