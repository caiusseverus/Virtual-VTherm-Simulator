from simulator.adapters.thermostat_adapter import ThermostatAdapter


def test_thermostat_hysteresis_command() -> None:
    t = ThermostatAdapter(target_temperature=20.0, hysteresis=0.2)
    t.update(19.7)
    assert t.get_heating_command() == 1.0
    t.update(20.3)
    assert t.get_heating_command() == 0.0
