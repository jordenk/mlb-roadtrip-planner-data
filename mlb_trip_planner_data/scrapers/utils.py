"""
Utility functions used for different scrapers.
"""

import json
import logging
from datetime import datetime
from minor_league_scraper  import get_minor_league_games
from mlb_scraper import get_mlb_games
from pytz import timezone
from splinter import Browser

def get_content_list(soup_list):
    return list(filter(lambda f: f, map(lambda m: m.string, soup_list)))


def date_string_to_timestamp(year, month, day, time_str):
    """
    example parameters (2019, 1, 31, "9:45 PM MST")
    """
    TZ_OFFSET_MAP = {
        'EDT': 'US/Eastern',
        'EST': 'US/Eastern',
        'ET': 'US/Eastern',
        'CDT': 'US/Central',
        'CST': 'US/Central',
        'CT': 'US/Central',
        'MDT': 'US/Mountain',
        'MST': 'US/Mountain',
        'MT': 'US/Mountain',
        'PDT': 'US/Pacific',
        'PST': 'US/Pacific',
        'PT': 'US/Pacific'
    }
    year = int(year)
    month = int(month)
    day = int(day)

    if 'TBD' in time_str:
        logging.info("Found a TBD game. Timestamp will be recorded as 3AM Eastern.")
        dt = datetime(year=year, month=month, day=day, hour=3)
        return int(timezone('US/Eastern').localize(dt).timestamp())
    
    time_arr = time_str.split(' ')
    assert len(time_arr) == 3
    time = datetime.strptime(' '.join(time_arr[:2]), '%I:%M %p')
    tz = TZ_OFFSET_MAP[time_arr[2]]

    dt = datetime(year=year, month=month, day=day, hour=time.hour, minute=time.minute)
    local_dt = timezone(tz).localize(dt)
    return int(local_dt.timestamp())


def write_dict_list_to_file(data, path, mode='a'):
    with open(path, mode) as f:
        json_list = map(lambda d: json.dumps(d) + '\n', data)
        f.writelines(json_list)


def write_games_to_file_system(team_data) -> None:
    """
    Wrapper function to make parallel calls easier. Uses a single browser process to get all games for
    a team.
    """
    browser = Browser('chrome', headless=True)
    try:
        logging.info(f"{team_data.team} - {team_data.year} Starting write...")
        for month in list(range(team_data.start_month, team_data.end_month + 1)):
            # Handle branching here so we don't have to pass functions with the multiprocess module.
            data = None
            if type(team_data) == BaseScheduleScraperData:
                data = get_mlb_games(browser, team_data.team, team_data.year, month)
            elif type(team_data) == MinorLeagueScheduleScraperData:
                data = get_minor_league_games(browser, team_data.id, team_data.year, month)
            else:
                raise TypeError(f"{type(team_data)} is not a supported type.")
            write_dict_list_to_file(data, f"{team_data.output_directory}/{team_data.team}.jsonl")
    finally:
        browser.quit()
    logging.info(f"{team_data.team} - {team_data.year} Completed successfully.")


class BaseScheduleScraperData:
    """
    Class used to group fields used for parallel functions.
    """
    def __init__(self, team, year, start_month, end_month, output_directory):
        self.team = team
        self.year = year
        self.start_month = start_month
        self.end_month = end_month
        self.output_directory = output_directory


class MinorLeagueScheduleScraperData(BaseScheduleScraperData):
    def __init__(self, team, year, start_month, end_month, output_directory, id):
        super().__init__(team, year, start_month, end_month, output_directory)
        self.id = id
