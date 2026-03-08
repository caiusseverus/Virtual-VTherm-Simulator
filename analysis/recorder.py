"""CSV recording utility for simulation outputs."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class Recorder:
    """Write simulation rows to a CSV file."""

    def write_csv(self, rows: list[dict[str, Any]], output_path: str) -> Path:
        if not rows:
            raise ValueError("No simulation data to record.")

        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        fieldnames = list(rows[0].keys())
        with out_path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        return out_path
