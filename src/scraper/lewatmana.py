"""Scraper for facility listings on lewatmana.com.

A single, parametrized implementation covers every facility category exposed
under ``/lokasi/fasilitas-kesehatan/`` (pharmacies, hospitals, and so on).
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from pathlib import Path

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from .config import ScraperConfig
from .driver import build_chrome_driver
from .helpers import write_dicts_to_csv

BASE_URL = "https://lewatmana.com/lokasi/fasilitas-kesehatan/{category}/"
SEARCH_BOX_XPATH = '//*[@id="poi-search-by-category-query"]'
RESULT_FIELDS = ("title", "link", "address")
NEXT_PAGE_DELAY_SECONDS = 2


@dataclass(frozen=True)
class FacilityRecord:
    """A single facility entry scraped from a listing page."""

    title: str
    link: str
    address: str


def _submit_empty_search(driver: WebDriver) -> None:
    """Trigger the listing by submitting an empty search query."""
    search = driver.find_element(By.XPATH, SEARCH_BOX_XPATH)
    search.send_keys("")
    search.send_keys(Keys.RETURN)


def _extract_page_records(wait: WebDriverWait) -> list[FacilityRecord]:
    """Parse all facility entries visible on the current page."""
    left = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".related_poi_left"))
    )
    right = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".related_poi_right"))
    )

    records: list[FacilityRecord] = []
    for element in left + right:
        heading = element.find_element(By.TAG_NAME, "h3")
        link = heading.find_element(By.TAG_NAME, "a").get_attribute("href")
        address = element.find_element(By.TAG_NAME, "p").text.replace("\n", ", ")
        records.append(
            FacilityRecord(title=heading.text, link=link or "", address=address)
        )
    return records


def _go_to_next_page(driver: WebDriver, config: ScraperConfig) -> bool:
    """Advance to the next results page. Return ``False`` when none remain."""
    pagination_items = driver.find_elements(
        By.CSS_SELECTOR, "#pagination-container ul li"
    )
    if not pagination_items:
        return False

    next_button_xpath = (
        f'//*[@id="pagination-container"]/ul/li[{len(pagination_items)}]/a'
    )
    try:
        next_button = WebDriverWait(driver, config.element_timeout).until(
            EC.presence_of_element_located((By.XPATH, next_button_xpath))
        )
    except TimeoutException:
        return False

    if not (next_button.is_enabled() and next_button.is_displayed()):
        return False

    previous_url = driver.current_url
    next_button.click()
    time.sleep(NEXT_PAGE_DELAY_SECONDS)
    return driver.current_url != previous_url


def scrape_facilities(category: str, config: ScraperConfig) -> list[FacilityRecord]:
    """Scrape every facility of ``category`` across all paginated pages."""
    driver = build_chrome_driver(config)
    records: list[FacilityRecord] = []
    try:
        driver.get(BASE_URL.format(category=category))
        time.sleep(config.page_load_wait)
        _submit_empty_search(driver)

        wait = WebDriverWait(driver, config.element_timeout)
        while True:
            records.extend(_extract_page_records(wait))
            print(f"collected {len(records)} records so far")
            if not _go_to_next_page(driver, config):
                break
    finally:
        driver.quit()
    return records


def save_facilities(records: list[FacilityRecord], destination: Path) -> Path:
    """Persist scraped facility records to a CSV file."""
    return write_dicts_to_csv(
        [asdict(record) for record in records], RESULT_FIELDS, destination
    )
