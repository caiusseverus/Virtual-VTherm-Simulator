from simulator.scenarios.scenario_loader import load_scenario


def test_scenario_loader_reads_yaml() -> None:
    scenario = load_scenario("scenarios/winter_test.yaml")
    assert scenario.name == "winter_test"
    assert scenario.simulation.step_seconds == 10


def test_scenario_loader_reads_flat_legacy_yaml() -> None:
    scenario = load_scenario("scenarios/winter_day.yaml")
    assert scenario.name == "winter_day"
    assert scenario.weather.outdoor_amplitude_c == 5.0
    assert scenario.heating.max_power_kw == 5.0
