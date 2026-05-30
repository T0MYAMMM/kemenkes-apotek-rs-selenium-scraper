"""Filesystem and CSV helper utilities."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Mapping, Sequence


def ensure_directory(path: Path) -> Path:
    """Create ``path`` (and parents) if it does not already exist."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_dicts_to_csv(
    rows: Sequence[Mapping[str, str]],
    fieldnames: Sequence[str],
    destination: Path,
) -> Path:
    """Write a sequence of mappings to ``destination`` as UTF-8 CSV."""
    ensure_directory(destination.parent)
    with destination.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=list(fieldnames), quoting=csv.QUOTE_MINIMAL
        )
        writer.writeheader()
        writer.writerows(rows)
    return destination
