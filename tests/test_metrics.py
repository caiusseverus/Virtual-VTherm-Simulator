from simulator.metrics.metrics import summarize


def test_metrics_summary_uses_recorded_rows() -> None:
    rows = [
        {
            "indoor_temperature": 19.5,
            "target_temperature": 20.0,
            "heating_output": 1.0,
            "energy_consumption": 0.3,
        },
        {
            "indoor_temperature": 20.2,
            "target_temperature": 20.0,
            "heating_output": 0.0,
            "energy_consumption": 0.3,
        },
    ]
    summary = summarize(rows, step_seconds=60)
    assert summary.heating_duty_cycle == 0.5
    assert summary.energy_usage_kwh == 0.3
