async function runSimulation() {
  const req = {
    scenario: {
      name: "web_run",
      simulation: {
        duration_hours: Number(document.getElementById("duration").value),
        step_seconds: Number(document.getElementById("step").value),
      },
      building: {
        initial_indoor_temp: Number(document.getElementById("initial").value),
        thermal_mass: Number(document.getElementById("mass").value),
        heat_loss: Number(document.getElementById("loss").value),
      },
      weather: { outdoor_temp: Number(document.getElementById("outdoor").value) },
      heating: { max_power_kw: Number(document.getElementById("power").value) },
      thermostat: {
        target_temp: Number(document.getElementById("target").value),
        hysteresis: Number(document.getElementById("hysteresis").value),
      },
    },
  };

  document.getElementById("status").textContent = "Running simulation...";
  const res = await fetch("/simulate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  const payload = await res.json();

  document.getElementById("status").textContent = `Done in ${payload.runtime_seconds.toFixed(3)}s (speedup ${payload.speedup_factor.toFixed(1)}x)`;

  const csvText = await fetch(`/${payload.csv}`).then((r) => r.text());
  const rows = csvText.trim().split("\n").slice(1).map((line) => line.split(",").map(Number));
  const times = rows.map((r) => r[0] / 3600.0);
  const indoor = rows.map((r) => r[1]);
  const target = rows.map((r) => r[3]);
  const heating = rows.map((r) => r[4]);

  renderChart("tempChart", "Temperature", times, [
    { label: "Indoor", data: indoor, borderColor: "#2563eb" },
    { label: "Target", data: target, borderColor: "#f59e0b" },
  ]);
  renderChart("heatChart", "Heating Output", times, [
    { label: "Heating", data: heating, borderColor: "#dc2626" },
  ]);
}

const charts = {};
function renderChart(canvasId, title, labels, datasets) {
  if (charts[canvasId]) charts[canvasId].destroy();
  charts[canvasId] = new Chart(document.getElementById(canvasId), {
    type: "line",
    data: { labels, datasets },
    options: {
      responsive: true,
      plugins: { title: { display: true, text: title } },
      scales: { x: { title: { display: true, text: "Time (h)" } } },
    },
  });
}

document.getElementById("runBtn").addEventListener("click", runSimulation);
