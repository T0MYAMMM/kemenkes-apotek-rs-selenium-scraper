"""Scraper for the Indonesian Wikipedia list of hospitals."""

from __future__ import annotations

import time
from pathlib import Path

import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from .config import ScraperConfig
from .driver import build_chrome_driver
from .helpers import ensure_directory

WIKIPEDIA_URL = "https://id.wikipedia.org/wiki/Daftar_rumah_sakit_di_Indonesia"

# Human-readable labels applied to the tables in document order. When the page
# layout changes and more tables appear, extra tables fall back to a generic
# ``table_<index>`` name instead of raising.
TABLE_NAMES = [
    "Berdasarkan Penyelenggara",
    "Berdasarkan Jenis Pelayanan",
    "Aceh",
    "Bali",
    "Banten",
    "Bengkulu",
    "Daerah Istimewa Yogyakarta",
    "Daerah Khusus Ibu kota Jakarta",
    "Jakarta Barat",
    "Jakarta Pusat",
    "Jakarta Selatan",
    "Jakarta Timur",
    "Jakarta Utara",
    "Kepulauan Seribu",
    "Gorontalo",
    "Jambi",
    "Jawa Barat",
    "Jawa Tengah",
    "Jawa Timur",
    "Kalimantan Barat",
    "Kalimantan Selatan",
    "Kalimantan Tengah",
    "Kalimantan Timur",
    "Kalimantan Utara",
    "Kepulauan Bangka Belitung",
    "Kepulauan Riau",
    "Lampung",
    "Maluku",
    "Maluku Utara",
    "Nusa Tenggara Barat",
    "Nusa Tenggara Timur",
    "Papua",
    "Papua Barat",
    "Riau",
    "Sulawesi Barat",
    "Sulawesi Selatan",
    "Sulawesi Tengah",
    "Sulawesi Tenggara",
    "Sulawesi Utara",
    "Sumatera Barat",
    "Sumatera Selatan",
    "Sumatera Utara",
]


def _table_to_dataframe(table: WebElement) -> pd.DataFrame | None:
    """Convert a single HTML table element into a DataFrame.

    Return ``None`` when the table has no header row or contains no data rows
    that match the header width.
    """
    rows = table.find_elements(By.TAG_NAME, "tr")
    if not rows:
        return None

    header = [cell.text for cell in rows[0].find_elements(By.TAG_NAME, "th")]
    if not header:
        return None

    data: list[list[str]] = []
    for row in rows[1:]:
        values = [cell.text for cell in row.find_elements(By.TAG_NAME, "td")]
        if len(values) == len(header):
            data.append(values)

    if not data:
        return None
    return pd.DataFrame(data, columns=header)


def scrape_hospital_tables(config: ScraperConfig) -> list[pd.DataFrame]:
    """Scrape every well-formed hospital table from the Wikipedia article."""
    driver = build_chrome_driver(config)
    frames: list[pd.DataFrame] = []
    try:
        driver.get(WIKIPEDIA_URL)
        time.sleep(config.page_load_wait)
        for table in driver.find_elements(By.TAG_NAME, "table"):
            frame = _table_to_dataframe(table)
            if frame is not None:
                frames.append(frame)
    finally:
        driver.quit()
    return frames


def save_hospital_tables(frames: list[pd.DataFrame], output_dir: Path) -> list[Path]:
    """Write each scraped table to its own CSV file under ``output_dir``."""
    ensure_directory(output_dir)
    written: list[Path] = []
    for index, frame in enumerate(frames):
        name = TABLE_NAMES[index] if index < len(TABLE_NAMES) else f"table_{index}"
        destination = output_dir / f"tabel_{name}.csv"
        frame.to_csv(destination, index=False)
        written.append(destination)
    return written
