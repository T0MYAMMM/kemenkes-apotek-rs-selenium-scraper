# Indonesian Pharmacy and Hospital Scraper

A Selenium-based web scraper that collects publicly listed pharmacy (apotek) and
hospital (rumah sakit) data across Indonesia. It gathers facility names,
location links, and addresses from lewatmana.com, and structured hospital
tables from the Indonesian Wikipedia. Results are exported as CSV files for
further analysis.

## Architecture / Tech Stack

- Language: Python 3.9+
- Browser automation: Selenium (Chrome WebDriver)
- Data handling: pandas
- Configuration: python-dotenv

The project follows a `src/` layout. A single parametrized module handles every
lewatmana.com facility category, while a dedicated module parses Wikipedia
hospital tables. Runtime behavior is driven entirely by environment variables.

## Project Structure

```
.
├── main.py                     # Entry point for running without installation
├── pyproject.toml              # Packaging and dependencies
├── requirements.txt            # Pinned runtime dependencies
├── .env.example                # Sample environment configuration
├── assets/
│   └── extension_5_8_0_0.crx   # Optional Chrome extension
├── data/
│   ├── reference/              # Static reference datasets
│   └── output/                 # Scraped CSV output
│       ├── apotek/
│       └── rumah_sakit/
└── src/
    └── scraper/
        ├── cli.py              # Command-line interface
        ├── config.py           # Environment-driven configuration
        ├── driver.py           # Chrome WebDriver factory
        ├── helpers.py          # Filesystem and CSV utilities
        ├── lewatmana.py        # lewatmana.com facility scraper
        └── wikipedia.py        # Wikipedia hospital-table scraper
```

## Local Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/T0MYAMMM/kemenkes-apotek-rs-selenium-scraper.git
   cd kemenkes-apotek-rs-selenium-scraper
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate    # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Alternatively, install the project as a package to expose the
   `apotek-rs-scraper` command:

   ```bash
   pip install -e .
   ```

4. Create a local configuration from the template:

   ```bash
   cp .env.example .env
   ```

   Google Chrome must be installed. A matching ChromeDriver is resolved
   automatically by Selenium Manager, so no manual driver download is required.

## Usage

Run a scraper by selecting a data source:

```bash
python main.py apotek                    # Pharmacies from lewatmana.com
python main.py rumah-sakit-lewatmana     # Hospitals from lewatmana.com
python main.py rumah-sakit-wikipedia     # Hospital tables from Wikipedia
python main.py all                       # Run every scraper in sequence
```

If the package was installed with `pip install -e .`, the same commands are
available through the console script:

```bash
apotek-rs-scraper apotek
```

Output CSV files are written under the directory configured by `OUTPUT_DIR`
(default `data/output`).

### Configuration

All settings are read from environment variables (see `.env.example`):

| Variable                | Description                                         | Default              |
| ----------------------- | --------------------------------------------------- | -------------------- |
| `HEADLESS`              | Run Chrome without a visible window.                | `false`              |
| `CHROMEDRIVER_PATH`     | Explicit ChromeDriver path (optional).              | auto-resolved        |
| `CHROME_EXTENSION_PATH` | Optional `.crx` extension to load.                  | empty                |
| `OUTPUT_DIR`            | Directory for scraped CSV files.                    | `data/output`        |
| `PAGE_LOAD_WAIT`        | Seconds to wait after each page load.               | `10`                 |
| `ELEMENT_TIMEOUT`       | Maximum seconds to wait for an element.             | `10`                 |

## Future Improvements

- Replace fixed `time.sleep` delays with explicit waits driven by page state.
- Derive Wikipedia table names from section headings instead of a static list.
- Add automated tests with mocked WebDriver interactions.
- Introduce structured logging in place of print statements.
- Support additional facility categories and alternative export formats.
- Containerize the scraper for reproducible, headless execution in CI.
