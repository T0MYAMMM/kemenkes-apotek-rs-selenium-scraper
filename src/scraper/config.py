"""Runtime configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # python-dotenv is optional at runtime
    pass

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "output"


def _get_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _get_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    return int(value)


@dataclass
class ScraperConfig:
    """Centralized, environment-driven settings for every scraper."""

    headless: bool = field(default_factory=lambda: _get_bool("HEADLESS", False))
    chromedriver_path: str | None = field(
        default_factory=lambda: os.getenv("CHROMEDRIVER_PATH") or None
    )
    chrome_extension_path: str | None = field(
        default_factory=lambda: os.getenv("CHROME_EXTENSION_PATH") or None
    )
    output_dir: Path = field(
        default_factory=lambda: Path(os.getenv("OUTPUT_DIR", str(DEFAULT_OUTPUT_DIR)))
    )
    page_load_wait: int = field(default_factory=lambda: _get_int("PAGE_LOAD_WAIT", 10))
    element_timeout: int = field(default_factory=lambda: _get_int("ELEMENT_TIMEOUT", 10))

    @classmethod
    def from_env(cls) -> "ScraperConfig":
        """Build a configuration instance from the current environment."""
        return cls()
