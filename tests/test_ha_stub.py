from datetime import datetime, timedelta

from simulator.ha_stub import HARuntime, register_climate_services


def test_state_machine_get_set_round_trip() -> None:
    runtime = HARuntime()
    runtime.states.set("sensor.example", 12.3, {"unit": "kW"})

    state = runtime.states.get("sensor.example")
    assert state is not None
    assert state.state == 12.3
    assert state.attributes["unit"] == "kW"


def test_runtime_uses_controllable_sim_time() -> None:
    now = datetime(2024, 1, 1, 0, 0, 0)

    def _now() -> datetime:
        return now

    runtime = HARuntime(now=_now)
    state1 = runtime.states.set("sensor.clocked", "a")
    assert state1.last_changed == datetime(2024, 1, 1, 0, 0, 0)

    nonlocal_now = {"value": now}

    def _now_dynamic() -> datetime:
        return nonlocal_now["value"]

    runtime2 = HARuntime(now=_now_dynamic)
    runtime2.states.set("sensor.clocked", "a")
    nonlocal_now["value"] = now + timedelta(seconds=15)
    state2 = runtime2.states.set("sensor.clocked", "b")
    assert state2.last_changed == datetime(2024, 1, 1, 0, 0, 15)


def test_climate_services_turn_on_turn_off_and_set_temperature() -> None:
    runtime = HARuntime()
    register_climate_services(runtime, initial_temperature=19.0)

    runtime.services.call("climate", "set_temperature", {"temperature": 21.5})
    climate = runtime.states.get("climate.simulated_thermostat")
    assert climate is not None
    assert climate.attributes["temperature"] == 21.5

    runtime.services.call("climate", "turn_on", {})
    climate = runtime.states.get("climate.simulated_thermostat")
    assert climate is not None
    assert climate.state == "heat"
    assert climate.attributes["hvac_mode"] == "heat"

    runtime.services.call("climate", "turn_off", {})
    climate = runtime.states.get("climate.simulated_thermostat")
    assert climate is not None
    assert climate.state == "off"
    assert climate.attributes["hvac_mode"] == "off"
