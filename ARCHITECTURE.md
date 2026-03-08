# Architecture

This repository now treats `simulator/*` as the canonical stack.

## Canonical modules

- `simulator/core`
  - `simulation_engine.py`: orchestrates thermostat decisions, weather, thermal updates, HA state publication, and metrics capture.
  - `time_controller.py` + `scheduler.py`: deterministic simulation time and callback scheduling.
- `simulator/scenarios`
  - `scenario_loader.py`: loads YAML, normalizes both legacy flat and canonical nested schemas.
  - `scenario_schema.py`: typed scenario dataclasses.
- `simulator/thermal`
  - `building_model.py`: single-node thermal dynamics with optional solar/internal gains.
  - `weather_model.py`: constant and sinusoidal outdoor models.
  - `heat_source.py`: converts thermostat command ratio to power.
- `simulator/adapters`
  - `thermostat_adapter.py`: controller contract implementation.
  - `ha_runtime.py`: Home Assistant-like state/event/service stubs used during simulation.
- `simulator/metrics`
  - `metrics.py`: timestep recorder (CSV/dataframe-like export) plus summary KPIs.
- `simulator/visualization`
  - `plotter.py`: temperature, heating, and energy plots.
- `simulator/web`
  - `api.py` + `server.py`: FastAPI endpoints + static frontend serving.

## Legacy to canonical mapping

| Legacy area | Canonical equivalent |
|---|---|
| `sim/engine.py` | `simulator/core/simulation_engine.py` |
| `sim/scenario.py` | `simulator/scenarios/scenario_loader.py` + `scenario_schema.py` |
| `sim/metrics.py` | `simulator/metrics/metrics.py` |
| `sim/sensors.py` | `simulator/thermal/weather_model.py` |
| `fake_ha/*` | `simulator/adapters/ha_runtime.py` |
| `web/app.py` | `simulator/web/server.py` (`uvicorn simulator.web.server:app`) |
| `run_sim.py` and experiment wrappers | `run_simulation.py` |
| `analysis/*` + `visualization/*` | `simulator/metrics/*` + `simulator/visualization/*` |

## Extension points

- Add richer weather profiles by introducing new weather model classes exposing `get_temperature(time_s) -> float`.
- Swap thermostat logic by extending/replacing `simulator.adapters.thermostat_adapter.ThermostatAdapter`.
- Add new outputs by extending `MetricsRecorder.record(...)` fields and updating `plotter.py`.
- Integrate additional HA behavior by expanding `HARuntime` (services/events/states) while preserving deterministic execution.
