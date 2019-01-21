"""
Scraper for Minor League games.
"""

import logging
import os
import re

from bs4 import BeautifulSoup
from utils import date_string_to_timestamp


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


def write_to_file(data, path):
    with open(path, 'w') as f:
        newline_list = map(lambda d: d + '\n', data)
        f.writelines(newline_list)


def get_id(tag):
    name = tag.text
    # FIXME get ids working with BS
    links = list(filter(lambda s: "http://www.milb.com/index.jsp?sid" in s, str(tag).split(" ")))
    assert len(links) == 1, f"Could not parse the team id: {name}"
    return links[0].split("sid=")[1].rstrip('"')


def get_minor_league_games(browser, id, year, month):
    """
    Scrapes one month of games from the calendar view. Returns a list of dicts.
    Double header support is not enabled.
    """
    games = []
    link = f"http://www.milb.com/schedule/index.jsp?sid={id}&m={month}&y={year}"
    browser.visit(link)
    soup = BeautifulSoup(browser.html, 'html.parser')

    dirty_name = list(filter(lambda s: 'team_name_short' in s, str(soup).splitlines()))[0]
    clean_short_name = dirty_name.replace('\t', '').replace('"', '').rstrip(',').split(':')[1]
    tz = get_timezone(soup, link)

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
            time = f"{game_info[1].text.strip()} {tz}"
            classes = game_elem[0].attrs.get('class')
            is_home_game = None
            if 'home' in classes and vs_or_at == 'vs':
                is_home_game = True
            elif 'away' in classes and vs_or_at == '@':
                is_home_game = False
            else:
                logging.error(f"See: {link} Date: {year}-{month}-{date}")
                raise Exception("Cannot determine if game is home or away.")

            # Game time handling
            timestamp = 0
            try:
                timestamp = date_string_to_timestamp(year, month, date, time)
            except Exception as e:
                logging.error(f"error processing data from: {link}")
                logging.warn(f"timestamp will be recorded as {timestamp}, see: team - {opponent} opponent - {opponent} {time}")
                logging.error(str(e))

            game = {'team': clean_short_name.lower(), 'opponent': opponent.lower(), 'opponent_tri_codes': None, 'is_home_game': is_home_game, 'game_start_time': timestamp}
            games.append(game)
    return games


def get_timezone(element, link):
    s = element.find('div', {'class': 'calendar-notice'})
    if s is None:
        logging.error(f"Could not find timezone: {link}")
    cal_notice = s.text
    matched = re.search('All times (.+?). Subject to change.', cal_notice)
    return matched.group(1) if matched else ''
