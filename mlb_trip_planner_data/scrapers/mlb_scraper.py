import json

from bs4 import BeautifulSoup
from splinter import Browser
from utils import date_string_to_timestamp, get_content_list, write_dict_list_to_file


def get_mlb_games(browser, team, year, month):
    """
    Scrapes one month of games from the calendar view. Returns a list of dicts.
    """
    games = []
    browser.visit(f"https://www.mlb.com/{team}/schedule/{year}-{month}")
    date_rows = BeautifulSoup(browser.html, 'html.parser').findAll('td', {'class': 'regular-season'})
    for row in date_rows:
        is_home_game = 'home' in row.attrs.get('class')
        day = row.find('div', {'class': 'day-of-month-label'}).contents[0]

        opponent_names = get_content_list(row.find_all('div', {'class': 'opponent-name'}))
        opponent_tri_codes = get_content_list(row.find_all('div', {'class': 'opponent-tricode'}))
        primary_times = get_content_list(row.find_all('div', {'class': 'primary-time'}))

        for on, otc, pt in zip(opponent_names, opponent_tri_codes, primary_times):
            timestamp = date_string_to_timestamp(year, month, day, pt)
            game = {'team': team, 'opponent': on, 'opponent_tri_codes': otc, 'is_home_game': is_home_game, 'game_start_time': timestamp}
            games.append(game)
    return games


browser = Browser('chrome', headless=True)
try:
    data = get_mlb_games(browser, 'dodgers', 2019, 4)
    write_dict_list_to_file(data, 'here.jsonl')
finally:
    browser.quit()
