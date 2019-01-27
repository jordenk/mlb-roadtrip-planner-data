# Description
Used to plan MLB road trips.

The scraping/extraction entry point is: `mlb_trip_planner_data/scrapers/multiprocess_runner.py`
The runner uses the Selenium web driver with chrome to scrape baseball schedules. This is done in parallel. Selenium is not thread safe, so separate processes must be run. The number of process that can be run is NUMBER_OF_CORES - 1.

Complete:
- MLB data extraction
- Minor leagues data extraction

In-progress:
- MLB data cleaning

Planned:
- Handle international games
- Populate Elasticsearch with game data, allowing map displays.
- Populate Neo4j with game data and driving time between games.

# Install dependencies
## Python dependencies (3.7)
$ pipenv install

## Chrome driver
Mac:
`$ brew cask install chromedriver`
TODO package this rather than requiring an install

# Scrape data
All games are scraped, home and away. This duplication allows for filling in missing data and during the transform step.
TODO change this script to a main file
`$ python3 mlb_trip_planner_data/scrapers/multiprocess_runner.py`

## Output
Data is written to `raw_data/{level}/{year}/{team}.jsonl`

# Testing
Testing is limited. Run with:
`$python3 -m pytest`

Scraping data depends on constant html elements and website uptime. Logging for data quality alerts. Some data may need to be fixed manually.