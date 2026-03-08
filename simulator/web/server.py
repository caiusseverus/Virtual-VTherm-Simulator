"""FastAPI server entrypoint."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from simulator.web.api import router

app = FastAPI(title="Thermostat Simulator")
app.include_router(router)

frontend_dir = Path(__file__).parent / "frontend"
results_dir = Path("simulator/results")
results_dir.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
app.mount("/simulator/results", StaticFiles(directory=results_dir), name="results")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(frontend_dir / "index.html")
