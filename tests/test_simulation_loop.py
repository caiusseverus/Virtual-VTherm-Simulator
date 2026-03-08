from simulator.core.simulation_engine import SimulationEngine
from simulator.scenarios.scenario_loader import load_scenario


def test_simulation_loop_records_steps() -> None:
    scenario = load_scenario("scenarios/cold_snap.yaml")
    engine = SimulationEngine(scenario)
    result = engine.run()
    df = result.metrics.to_dataframe()
    expected_steps = int(scenario.simulation.duration_hours * 3600 / scenario.simulation.step_seconds)
    assert len(df) == expected_steps
    assert result.runtime_seconds >= 0


def test_simulation_loop_supports_variable_weather_profile() -> None:
    scenario = load_scenario("scenarios/winter_day.yaml")
    engine = SimulationEngine(scenario)
    result = engine.run()
    df = result.metrics.to_dataframe()
    assert max(df["outdoor_temperature"]) > min(df["outdoor_temperature"])
