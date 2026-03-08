from simulator.thermal.building_model import BuildingModel


def test_building_model_stability_toward_outdoor_temp_without_heating() -> None:
    model = BuildingModel(indoor_temperature=25.0, thermal_mass=150000, heat_loss_coefficient=220)
    for _ in range(360):
        model.step(dt_s=10, outdoor_temperature=5, heating_power_w=0)
    assert model.indoor_temperature < 25.0
    assert model.indoor_temperature > 5.0
