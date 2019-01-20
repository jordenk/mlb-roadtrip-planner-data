# Install dependencies
pip3 install -r requirements.txt

# Data Population
## MLB
 python3 mlb_trip_planner_data/scrapers/mlb_scraper.py

## AAA
AAA schedules are scrapbed from online schedues.


# Testing
python3 -m pytest