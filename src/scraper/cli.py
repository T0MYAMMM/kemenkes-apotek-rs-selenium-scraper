"""Command-line interface for the health-facility scrapers."""

from __future__ import annotations

import argparse

from .config import ScraperConfig
from .lewatmana import save_facilities, scrape_facilities
from .wikipedia import save_hospital_tables, scrape_hospital_tables


def _run_apotek(config: ScraperConfig) -> None:
    records = scrape_facilities("apotek", config)
    destination = config.output_dir / "apotek" / "data_apotek_seluruh_indonesia.csv"
    path = save_facilities(records, destination)
    print(f"Saved {len(records)} pharmacies to {path}")


def _run_rumah_sakit_lewatmana(config: ScraperConfig) -> None:
    records = scrape_facilities("rumah-sakit", config)
    destination = (
        config.output_dir / "rumah_sakit" / "data_rumah_sakit_seluruh_indonesia.csv"
    )
    path = save_facilities(records, destination)
    print(f"Saved {len(records)} hospitals to {path}")


def _run_rumah_sakit_wikipedia(config: ScraperConfig) -> None:
    frames = scrape_hospital_tables(config)
    output_dir = config.output_dir / "rumah_sakit"
    paths = save_hospital_tables(frames, output_dir)
    print(f"Saved {len(paths)} hospital tables to {output_dir}")


COMMANDS = {
    "apotek": _run_apotek,
    "rumah-sakit-lewatmana": _run_rumah_sakit_lewatmana,
    "rumah-sakit-wikipedia": _run_rumah_sakit_wikipedia,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Scrape Indonesian pharmacy and hospital data."
    )
    parser.add_argument(
        "source",
        choices=[*COMMANDS, "all"],
        help="Which data source to scrape.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    config = ScraperConfig.from_env()

    targets = COMMANDS.values() if args.source == "all" else [COMMANDS[args.source]]
    for run in targets:
        run(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
