"""
Utility functions used for different scrapers.
"""

import json
import logging
from datetime import datetime
from pytz import timezone

def get_content_list(soup_list):
    return list(filter(lambda f: f, map(lambda m: m.string, soup_list)))

def date_string_to_timestamp(year, month, day, time_str):
    """
    example parameters (2019, 1, 31, "9:45 PM MST")
    """
    TZ_OFFSET_MAP = {
        'EDT': 'US/Eastern',
        'EST': 'US/Eastern',
        'CDT': 'US/Central',
        'CST': 'US/Central',
        'MDT': 'US/Mountain',
        'MST': 'US/Mountain',
        'PDT': 'US/Pacific',
        'PST': 'US/Pacific'
    }
    year = int(year)
    month = int(month)
    day = int(day)


    if time_str == 'TBD':
        logging.info("Found a TBD game. Timestamp will be recorded as 3AM Eastern.")
        dt = datetime(year=year, month=month, day=day, hour=3)
        return int(timezone('US/EASTERN').localize(dt).timestamp())
    
    time_arr = time_str.split(' ')
    assert len(time_arr) == 3
    time = datetime.strptime(' '.join(time_arr[:2]), '%I:%M %p')
    tz = TZ_OFFSET_MAP[time_arr[2]]

    dt = datetime(year=year, month=month, day=day, hour=time.hour, minute=time.minute)
    local_dt = timezone(tz).localize(dt)
    return int(local_dt.timestamp())

def write_dict_list_to_file(data, path):
    with open(path, 'a') as f:
        json_list = map(lambda d: json.dumps(d) + '\n', data)
        f.writelines(json_list)

class TeamScheduleScraperData:
    """
    Class used to group fields used for parallel functions.
    """
    def __init__(self, team, year, start_month, end_month, output_directory):
        self.team = team
        self.year = year
        self.start_month = start_month
        self.end_month = end_month
        self.output_directory = output_directory