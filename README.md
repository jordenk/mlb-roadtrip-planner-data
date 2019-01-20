# Install dependencies
pip3 install -r requirements.txt

# Data Population
## MLB
Major Leagues schedules are derived from CSV drops. The MLB online schedules populate data dynamically, and I couldn't find a way to scrape data from those.

## AAA
AAA schedules are scrapbed from online schedues.


# Testing
python3 -m pytest