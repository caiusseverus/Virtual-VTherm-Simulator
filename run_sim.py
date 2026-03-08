"""Deprecated CLI compatibility wrapper.

Use `python run_simulation.py <scenario>` instead.
"""

from __future__ import annotations

import warnings

from run_simulation import main


if __name__ == "__main__":
    warnings.warn(
        "run_sim.py is deprecated; use run_simulation.py",
        DeprecationWarning,
        stacklevel=2,
    )
    main()
