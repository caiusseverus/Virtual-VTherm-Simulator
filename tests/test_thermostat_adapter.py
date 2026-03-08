from pathlib import Path

from simulator.adapters.ha_runtime import HARuntime
from simulator.adapters.thermostat_adapter import ThermostatAdapter


def test_mock_thermostat_mode_hysteresis_and_ha_service_routing() -> None:
    runtime = HARuntime()
    t = ThermostatAdapter(
        target_temperature=20.0,
        hysteresis=0.2,
        mode="mock_thermostat",
        ha_runtime=runtime,
    )
    t.set_temperature(20.5)

    climate_state = runtime.states.get("climate.simulated_thermostat")
    assert climate_state is not None
    assert climate_state.attributes["temperature"] == 20.5

    t.update(20.2, outdoor_temperature=6.0, time_s=60)
    assert t.get_heating_command() == 1.0
    assert runtime.states.get("climate.simulated_thermostat").state == "heat"

    t.update(20.8, outdoor_temperature=6.0, time_s=120)
    assert t.get_heating_command() == 0.0
    assert runtime.states.get("climate.simulated_thermostat").state == "off"


def test_dynamic_adapter_mode_loads_module_from_path_and_revision(tmp_path: Path) -> None:
    module_path = tmp_path / "dyn_thermostat.py"
    module_path.write_text(
        """
class ThermostatIntegration:
    def __init__(self, target_temperature, hysteresis, revision=None):
        self.target_temperature = target_temperature
        self.revision = revision

    def set_temperature(self, target):
        self.target_temperature = target

    def compute_heating_command(self, payload):
        demand = payload["target_temperature"] - payload["current_temperature"]
        if self.revision == "rev-2":
            demand += 0.1
        return 1.0 if demand > 0 else 0.0
""",
        encoding="utf-8",
    )

    runtime = HARuntime()
    t = ThermostatAdapter(
        target_temperature=20.0,
        mode="dynamic",
        integration_module_path=str(module_path),
        integration_revision="rev-2",
        ha_runtime=runtime,
    )

    t.set_temperature(20.0)
    t.update(20.05, outdoor_temperature=2.0, time_s=30)
    assert t.get_heating_command() == 1.0
    assert runtime.states.get("climate.simulated_thermostat").state == "heat"


def test_dynamic_mode_requires_integration_module_path() -> None:
    try:
        ThermostatAdapter(target_temperature=20.0, mode="dynamic")
    except ValueError as exc:
        assert "integration_module_path" in str(exc)
    else:
        raise AssertionError("Expected ValueError for missing integration_module_path")
