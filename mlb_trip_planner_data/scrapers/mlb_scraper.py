"""
Scraper for MLB games.
"""

import logging

from bs4 import BeautifulSoup
from utils import date_string_to_timestamp, get_content_list


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
        opponent_tri_codes = get_content_list(row.find_all('div', {'class': 'opponent-tricode'}))
        primary_times = get_content_list(row.find_all('div', {'class': 'primary-time'}))

        for on, otc, pt in zip(opponent_names, opponent_tri_codes, primary_times):
            timestamp = 0
            try:
                timestamp = date_string_to_timestamp(year, month, day, pt)
            except Exception as e:
                logging.error(f"error processing data from: {link}")
                logging.info(f"timestamp will be recorded as {timestamp}, see: {on} {otc} {pt}")
                logging.error(str(e))
            game = {'team': team.lower(), 'opponent': on.lower(), 'opponent_tri_codes': otc, 'is_home_game': is_home_game, 'game_start_time': timestamp}
            games.append(game)
    return games

# def write_games_to_file_system(team_data: BaseScheduleScraperData) -> None:
#     """
#     Wrapper function to make parallel calls easier. Uses a single browser process to get all games for
#     a team.
#     """
#     browser = Browser('chrome', headless=True)
#     try:
#         logging.info(f"{team_data.team} - {team_data.year} Starting write...")
#         for month in list(range(team_data.start_month, team_data.end_month + 1)):
#             data = get_mlb_games(browser, team_data.team, team_data.year, str(month))
#             write_dict_list_to_file(data, f"{team_data.output_directory}/{team_data.team}.jsonl")
#     finally:
#         browser.quit()
#     logging.info(f"{team_data.team} - {team_data.year} Completed successfully.")
