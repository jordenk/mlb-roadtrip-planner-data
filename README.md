# Description
Used to plan MLB road trips.

Complete:
- MLB data extraction

In-progress:
- MLB data cleaning
- Minor leagues data extraction

Planned:
- Populate Elasticsearch with game data, allowing map displays.
- Populate Neo4j with game data and driving time between games.

# Install dependencies
`pip3 install -r requirements.txt`

# Data Population
## MLB
`$ python3 mlb_trip_planner_data/scrapers/multiprocess_runner.py`

## Minor
AAA schedules are scrapbed from online schedues.

## Output
Data is written to `raw_data/{level}/{year}/{team}.jsonl`

# Testing
Testing is limited. Run with:
`$python3 -m pytest`

Scraping data depends on constant html elements and website uptime. Logging for data quality alerts. Some data may need to be fixed manually.