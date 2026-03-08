from simulator.scenarios.scenario_loader import load_scenario


def test_scenario_loader_reads_yaml() -> None:
    scenario = load_scenario("scenarios/winter_test.yaml")
    assert scenario.name == "winter_test"
    assert scenario.simulation.step_seconds == 10
