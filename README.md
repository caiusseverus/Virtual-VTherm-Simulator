# Virtual VTherm Simulator

A lightweight, self-contained thermal simulation sandbox inspired by Home Assistant + Versatile Thermostat style integrations.

## What this provides

- A fake Home Assistant core with:
  - state machine
  - event bus
  - scheduler
  - base entity class
- Building and heating plant models.
- Simulation engine with:
  - simulation clock
  - scenario configuration
  - virtual sensors
- Analysis tools to:
  - record timesteps to CSV
  - generate quick plots from run outputs
- YAML scenarios you can run immediately.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_sim.py --scenario scenarios/winter_day.yaml --output output/winter_day.csv --plot
```

## Project layout

```text
fake_ha/         # Fake Home Assistant runtime primitives
models/          # Physical models (building + heating plant)
sim/             # Simulation engine and helpers
analysis/        # Recording and graphing tools
integrations/    # Integration loader utilities
scenarios/       # YAML scenarios
run_sim.py       # Main CLI entrypoint
```

## Notes

- The simulator intentionally uses simple first-order dynamics for readability.
- All modules are importable and intentionally implemented (no placeholders).
