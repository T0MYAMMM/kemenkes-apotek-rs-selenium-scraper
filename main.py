"""Entry point for running the scrapers without installing the package.

Usage:
    python main.py apotek
    python main.py rumah-sakit-lewatmana
    python main.py rumah-sakit-wikipedia
    python main.py all
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from scraper.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
