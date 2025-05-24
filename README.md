# SternSoupScraper

This project, named `SternSoupScraper`, is a personal data & web scraping project developed for my portfolio. It demonstrates the ability to extract structured data from websites using Python libraries such as `requests`, `BeautifulSoup`, and `pandas`. Dependency management is handled with `uv`.

## Project Description

The project currently consists of two main scripts:

1.  **Scraping Aquaman Villains:** This script extracts a list of Aquaman's enemies from a Wikipedia page, including their first appearance and a brief description.
2.  **Scraping US Presidents:** This script extracts information about US Presidents from another Wikipedia page, including their birth/death years, name, party, term start date, election year(s), vice president(s), and a brief description scraped from their individual Wikipedia pages.
3.  **Scraping 20th Century Wars:** This script extracts information from 3 different Wikipedia pages including relevant dates, names, involvements, and descriptions from the individual pages.


The scraped data is processed and stored in pandas DataFrames for potential further analysis or use.

## Features

* Extracts tabular data from Wikipedia pages.
* Utilizes `BeautifulSoup` for efficient HTML parsing.
* Uses `requests` to handle HTTP requests.
* Processes and cleans scraped data (e.g., removing bracketed text, handling duplicates in a simple manner).
* Stores extracted data in `pandas` DataFrames.
* Includes a basic rate-limiting mechanism (`time.sleep`) when scraping multiple pages (in the US Presidents script).

## Installation

To set up the project, you will need Python and `uv` installed.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/yoavstr/SternSoupScraper
    cd SternSoupScraper
    ```

2.  **Install dependencies using `uv`:**

    ```bash
    uv sync
    ```

    This will read the `requirements.txt` file (which you should create manually or generate) and install the necessary packages (`requests`, `beautifulsoup4`, `pandas`, `lxml`).


## Usage

You can run the individual scripts from your terminal.

1.  **To scrape Aquaman Villains:**

    ```bash
    python aquaman_villains.py
    ```

2.  **To scrape US Presidents:**

    ```bash
    python usa_presidents.py
    ```
3.  **To scrape US Presidents:**

    ```bash
    python 20th_century_wars.py
    ```

The scripts will print the resulting pandas DataFrames to the console. You can modify the scripts to save the data to a file (e.g., CSV, JSON) if needed.

## Dependencies

* `requests`: For making HTTP requests to fetch web page content.
* `beautifulsoup4`: For parsing HTML content.
* `lxml`: A fast XML/HTML parser, often used as a backend for BeautifulSoup.
* `pandas`: For data manipulation and analysis, specifically for working with DataFrames.
* `uv`: For fast dependency management and package installation.

Happy Scraping!