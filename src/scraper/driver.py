"""Chrome WebDriver factory."""

from __future__ import annotations

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from .config import ScraperConfig


def build_chrome_driver(config: ScraperConfig) -> webdriver.Chrome:
    """Create a configured Chrome WebDriver instance.

    When ``chromedriver_path`` is not provided, Selenium Manager resolves a
    matching driver automatically, so no manual download is required.
    """
    options = Options()
    if config.headless:
        options.add_argument("--headless=new")

    if config.chrome_extension_path and Path(config.chrome_extension_path).exists():
        options.add_extension(config.chrome_extension_path)

    if config.chromedriver_path:
        service = Service(executable_path=config.chromedriver_path)
        return webdriver.Chrome(service=service, options=options)

    return webdriver.Chrome(options=options)
