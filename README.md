# Virtual VTherm Simulator

Standalone Python framework for high-speed Home Assistant heating controller simulation.

## Highlights

- Deterministic discrete-time simulation loop (no realtime waits).
- Fake Home Assistant runtime (`states`, `services`, `config`, and controllable time).
- Thermal model adapter with configurable heat capacity, losses, gains, and heater power.
- Thermostat adapter interface (`update` + `compute_heating_command`).
- Metrics + graph generation (`metrics.json` + SVG chart output).
- Simple browser UI for parameter editing and one-click simulation runs.

## Quick start

```bash
python run_sim.py --scenario scenarios/winter_day.yaml --output results/run_001/simulation.csv --plot
```

Outputs:

```text
results/run_001/
  simulation.csv
  metrics.json
  temperature.svg
```

## Run the web UI

```bash
python -m web.app
# open http://localhost:8000
```

## Scenario format (YAML)

Nested format supported:

```yaml
name: baseline
start_time: "2025-01-01T00:00:00"
simulation:
  duration_hours: 72
  timestep_seconds: 60
  initial_indoor_temp: 19
building:
  heat_capacity: 30000000
  heat_loss_coefficient: 200
heating:
  max_power_kw: 12
weather:
  outdoor_base_c: 5
  outdoor_amplitude_c: 4
thermostat:
  target_temperature: 21
gains:
  solar_gain_kw: 0.0
  internal_heat_gain_kw: 0.5
```

Flat legacy scenarios remain supported.

## Project layout

```text
analysis/          # CSV recording
fake_ha/           # Fake Home Assistant primitives
sim/               # Engine + scenario + metrics
thermal_model/     # Thermal model adapter interface
thermostat/        # Thermostat adapter interface
visualization/     # Graph generation
web/               # Lightweight web UI
experiments/       # Experiment entrypoints
```
