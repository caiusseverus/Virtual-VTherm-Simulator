# Thermostat Offline Simulator

Standalone Python framework for high-speed Home Assistant heating controller simulation.

## Canonical stack

The canonical implementation lives under `simulator/*`.
Legacy modules (`sim/*`, `web/app.py`, `run_sim.py`) are kept only as deprecation shims.

## Quick start

```bash
python run_simulation.py scenarios/winter_test.yaml --output simulator/results/cli_run
```

Outputs:

```text
simulator/results/cli_run/
  metrics.csv
  temperature_vs_target.png
  heating_output.png
  energy_usage.png
```

## Run the web UI

```bash
uvicorn simulator.web.server:app --host 0.0.0.0 --port 8000
# open http://localhost:8000
```

## Scenario format (nested)

```yaml
name: baseline
simulation:
  duration_hours: 72
  step_seconds: 60
building:
  initial_indoor_temp: 19
  thermal_mass: 30000000
  heat_loss: 200
heating:
  max_power_kw: 12
weather:
  outdoor_temp: 5
  outdoor_base_c: 5
  outdoor_amplitude_c: 4
thermostat:
  target_temp: 21
  hysteresis: 0.2
gains:
  solar_gain_kw: 0.0
  internal_heat_gain_kw: 0.5
```

Legacy flat scenarios are still accepted by the loader.

## Project layout

```text
simulator/core/          # engine loop, scheduler, simulation time
simulator/scenarios/     # schema + YAML normalization/validation
simulator/thermal/       # weather, heat source, building thermal model
simulator/adapters/      # thermostat adapter + HA-like stubs
simulator/metrics/       # timeseries recording + run summary metrics
simulator/visualization/ # plot generation
simulator/web/           # FastAPI API + static frontend
```

See `ARCHITECTURE.md` for detailed module responsibilities and extension points.
