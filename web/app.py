"""Deprecated web wrapper.

Use `uvicorn simulator.web.server:app --reload`.
"""

from __future__ import annotations

import warnings


def main() -> None:
    warnings.warn(
        "web/app.py is deprecated; use simulator.web.server FastAPI app",
        DeprecationWarning,
        stacklevel=2,
    )
    try:
        import uvicorn  # type: ignore
    except Exception as exc:  # pragma: no cover - import-time environment issue
        raise RuntimeError("uvicorn is required to run the canonical web server") from exc

    uvicorn.run("simulator.web.server:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    main()
