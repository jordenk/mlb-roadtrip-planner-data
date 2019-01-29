"""
Scraper functions for MLB and minor league games.
"""
import logging
import os
import re

from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone


def get_mlb_games(browser, team, year, month):
    """
    Scrapes one month of games from the calendar view. Returns a list of dicts.
    """
    games = []
    link = f"https://www.mlb.com/{team}/schedule/{year}-{month}"
    browser.visit(link)
    date_rows = BeautifulSoup(browser.html, 'html.parser').findAll('td', {'class': 'regular-season'})
    for row in date_rows:
        is_home_game = 'home' in row.attrs.get('class')
        day = row.find('div', {'class': 'day-of-month-label'}).contents[0]

        # Get all games in a day- double header consideration.
        opponent_names = get_content_list(row.find_all('div', {'class': 'opponent-name'}))
        primary_times = get_content_list(row.find_all('div', {'class': 'primary-time'}))

        for on, pt in zip(opponent_names, primary_times):
            timestamp = 0
            try:
                timestamp = date_string_to_timestamp(year, month, day, pt)
            except Exception as e:
                logging.error(f"error processing data from: {link}")
                logging.info(f"timestamp will be recorded as {timestamp}, see: {on} {otc} {pt}")
                logging.error(str(e))
            game = {'team': team.lower(), 'opponent': on.lower(), 'is_home_game': is_home_game, 'game_start_time': timestamp}
            games.append(game)
    return games


def write_minor_league_team_ids(browser, output_directory, link='http://www.milb.com/milb/info/affiliations.jsp'):
    """
    Scrapes milb.com to get the ids for team names. Data should be written to the resources directory.
    """
    browser.visit(link)
    # Browser.status_code is not implemented. Use title loading as a successful load check.
    title = browser.title
    assert type(title) is str and len(title) > 0, f"Error loading page {link}"

    aaa_teams = []
    aa_teams = []
    a_adv_teams = []
    a_teams = []
    for li in BeautifulSoup(browser.html, 'html.parser').findAll('li'):
        contents = li.contents
        if ' (AAA)' in contents:
            aaa_teams.append(get_id(contents[1]))
        elif ' (AA)' in contents:
            aa_teams.append(get_id(contents[1]))
        elif ' (A Adv.)' in contents:
            a_adv_teams.append(get_id(contents[1]))
        elif ' (A)' in contents:
            a_teams.append(get_id(contents[1]))

    MLB_AFFILIATES_COUNT = 30
    assert len(aaa_teams) == MLB_AFFILIATES_COUNT
    assert len(aa_teams) == MLB_AFFILIATES_COUNT
    assert len(a_adv_teams) == MLB_AFFILIATES_COUNT
    assert len(a_teams) == MLB_AFFILIATES_COUNT
    write_to_file(aaa_teams, os.path.join(output_directory, 'aaa_ids.txt'))
    write_to_file(aa_teams, os.path.join(output_directory, 'aa_ids.txt'))
    write_to_file(a_adv_teams, os.path.join(output_directory, 'a_adv_ids.txt'))
    write_to_file(a_teams, os.path.join(output_directory, 'a_ids.txt'))


def get_minor_league_games(browser, id, year, month):
    """
    Scrapes one month of games from the calendar view. Returns a list of dicts.
    Double header support is not enabled. Times aren't supported, just dates.
    """
    games = []
    link = f"http://www.milb.com/schedule/index.jsp?sid={id}&m={month}&y={year}"
    browser.visit(link)
    soup = BeautifulSoup(browser.html, 'html.parser')

    dirty_name = list(filter(lambda s: 'team_name_short' in s, str(soup).splitlines()))[0]
    clean_short_name = dirty_name.replace('\t', '').replace('"', '').rstrip(',').split(':')[1]

    date_rows = soup.findAll('td')
    for row in date_rows:
        date = row.find('div', {'class': 'date'}).text.strip()
        game_elem = row.findAll('li', {'class': 'game'})

        # handle double headers
        for g in game_elem:
            game_info = g.findAll('div')
            opponent_arr = game_info[0].text.strip().split(' ')
            vs_or_at = opponent_arr[0]
            opponent = opponent_arr[1]
            classes = game_elem[0].attrs.get('class')
            is_home_game = None
            if 'home' in classes or vs_or_at == 'vs':
                is_home_game = True
            elif 'away' in classes or vs_or_at == '@':
                is_home_game = False
            else:
                logging.error(f"See: {link} Date: {year}-{month}-{date}")
                raise Exception("Cannot determine if game is home or away.")

            # Game time handling
            timestamp = 0
            try:
                timestamp = date_string_to_timestamp(year, month, date, 'TBD')
            except Exception as e:
                logging.error(f"error processing data from: {link}")
                logging.warn(f"timestamp will be recorded as {timestamp}, see: team - {team} opponent - {opponent}")
                logging.error(str(e))

            game = {'team': clean_short_name.lower(), 'opponent': opponent.lower(), 'is_home_game': is_home_game, 'game_start_time': timestamp}
            games.append(game)
    return games


# Helper functions
def get_content_list(soup_list):
    return list(filter(lambda f: f, map(lambda m: m.string, soup_list)))


def get_id(tag):
    name = tag.text
    # FIXME get ids working with BS
    links = list(filter(lambda s: "http://www.milb.com/index.jsp?sid" in s, str(tag).split(" ")))
    assert len(links) == 1, f"Could not parse the team id: {name}"
    return links[0].split("sid=")[1].rstrip('"')


def write_to_file(data, path):
    with open(path, 'w') as f:
        newline_list = map(lambda d: d + '\n', data)
        f.writelines(newline_list)


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
        logging.debug("Found a TBD game. Timestamp will be recorded as 3AM Eastern.")
        dt = datetime(year=year, month=month, day=day, hour=3)
        return int(timezone('US/Eastern').localize(dt).timestamp())

    time_arr = time_str.split(' ')
    assert len(time_arr) == 3
    time = datetime.strptime(' '.join(time_arr[:2]), '%I:%M %p')
    tz = TZ_OFFSET_MAP[time_arr[2]]

    dt = datetime(year=year, month=month, day=day, hour=time.hour, minute=time.minute)
    local_dt = timezone(tz).localize(dt)
    return int(local_dt.timestamp())
