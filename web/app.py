"""Simple web UI to edit parameters and run simulations."""

from __future__ import annotations

import json
from datetime import timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs

from analysis.recorder import Recorder
from sim.engine import SimulationEngine
from sim.metrics import summarize
from sim.scenario import SimulationScenario
from visualization.plots import create_temperature_plot


class SimulationHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if self.path.startswith("/results/"):
            file_path = Path(self.path.lstrip("/"))
            if file_path.exists():
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.end_headers()
                self.wfile.write(file_path.read_bytes())
                return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(self._page().encode("utf-8"))

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length).decode("utf-8")
        data = parse_qs(body)

        scenario = SimulationScenario(
            name="web_run",
            start_time=SimulationScenario.from_yaml("scenarios/winter_day.yaml").start_time,
            duration=timedelta(hours=float(data.get("duration_hours", ["24"])[0])),
            step_seconds=int(data.get("step_seconds", ["60"])[0]),
            indoor_initial_c=float(data.get("indoor_initial_c", ["19"])[0]),
            target_temp_c=float(data.get("target_temp_c", ["21"])[0]),
            outdoor_base_c=float(data.get("outdoor_base_c", ["5"])[0]),
            outdoor_amplitude_c=float(data.get("outdoor_amplitude_c", ["4"])[0]),
            building_heat_capacity=float(data.get("building_heat_capacity", ["30000000"])[0]),
            heat_loss_coefficient=float(data.get("heat_loss_coefficient", ["200"])[0]),
            heating_power_kw=float(data.get("heating_power_kw", ["12"])[0]),
        )
        rows = SimulationEngine(scenario).run()
        base = Path("results/web_run")
        csv_path = Recorder().write_csv(rows, str(base / "simulation.csv"))
        plot_path = create_temperature_plot(str(csv_path), str(base / "temperature.svg"))
        metrics = summarize(rows, scenario.step_seconds)
        (base / "metrics.json").write_text(json.dumps(metrics.__dict__, indent=2), encoding="utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(self._page(plot_path.as_posix(), metrics.__dict__).encode("utf-8"))

    def _page(self, plot: str | None = None, metrics: dict[str, float] | None = None) -> str:
        metrics_html = ""
        if metrics:
            items = "".join(f"<li><strong>{k}</strong>: {v:.3f}</li>" for k, v in metrics.items())
            metrics_html = f"<h3>Metrics</h3><ul>{items}</ul>"
        plot_html = f'<h3>Plot</h3><img src="/{plot}" width="900" />' if plot else ""
        return f"""
        <html><body>
        <h1>Virtual VTherm Simulator</h1>
        <form method='post'>
            Duration (hours): <input name='duration_hours' value='24'><br>
            Step (seconds): <input name='step_seconds' value='60'><br>
            Initial indoor °C: <input name='indoor_initial_c' value='19'><br>
            Target °C: <input name='target_temp_c' value='21'><br>
            Outdoor base °C: <input name='outdoor_base_c' value='5'><br>
            Outdoor amplitude °C: <input name='outdoor_amplitude_c' value='4'><br>
            Heat capacity: <input name='building_heat_capacity' value='30000000'><br>
            Heat loss coeff: <input name='heat_loss_coefficient' value='200'><br>
            Max heating kW: <input name='heating_power_kw' value='12'><br>
            <button type='submit'>Run Simulation</button>
        </form>
        {metrics_html}
        {plot_html}
        </body></html>
        """


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = HTTPServer((host, port), SimulationHandler)
    print(f"Web UI running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
