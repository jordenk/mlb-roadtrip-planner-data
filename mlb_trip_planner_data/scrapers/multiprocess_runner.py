import json
import logging
import os

from multiprocessing import Pool, cpu_count
from scrapers import get_mlb_games, write_minor_league_team_ids, get_minor_league_games
from splinter import Browser


# TODO Set up a central logger with configurable level
logging.basicConfig(level=logging.INFO)
# TODO Make this command line parameters
YEAR = 2019

# CONSTANTS
TEAM_COUNT = 30
START_MONTH = 3  # Different leagues start in different months, so this could be configurable.
END_MONTH = 9
MLB_SEASON_GAMES_COUNT = 162
MINOR_LEAGUE_ID_PATH = 'mlb_trip_planner_data/resources'
MINOR_LEAGUE_LEVELS = ['aaa', 'aa', 'a_adv', 'a']  # TODO Enum


def parallel_execution(function_arg, list_arg):
    max_processes = cpu_count() - 1
    with Pool(processes=max_processes) as pool:
        pool.map(function_arg, list_arg)


def execute_parallel_mlb():
    mlb_teams = [
        "angels", "astros", "athletics", "bluejays", "braves", "brewers", "cardinals", "cubs", "dbacks", "dodgers",
        "giants", "indians", "mariners", "marlins", "mets", "nationals", "orioles", "phillies", "padres", "pirates",
        "rangers", "rays", "reds", "redsox", "rockies", "royals", "tigers", "twins", "whitesox", "yankees"
        ]

    OUTPUT_DIRECTORY = f"raw_data/mlb/{YEAR}"

    parameter_object_list = list(map(lambda t: TeamScheduleScraperData(t, YEAR, START_MONTH, END_MONTH, OUTPUT_DIRECTORY), mlb_teams))
    assert len(parameter_object_list) == TEAM_COUNT, "Incorrect number of teams found. Stopping execution."

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    parallel_execution(write_games_to_file_system, parameter_object_list)

    logging.info("... Finished writing schedules")
    inspect_jsonl_files(OUTPUT_DIRECTORY, MLB_SEASON_GAMES_COUNT)


def execute_parallel_minor_league(id_file_name):
    ids = []
    with open(os.path.join(MINOR_LEAGUE_ID_PATH, id_file_name)) as f:
        data = f.readlines()
        ids = list(map(lambda i: i.rstrip('\n'), data))
    assert len(ids) == TEAM_COUNT, f"Incorrect number of ids read from file: {id_file_name}"

    OUTPUT_DIRECTORY = f"raw_data/{id_file_name.split('_ids')[0]}/{YEAR}"
    parameter_object_list = list(map(lambda id: TeamScheduleScraperData(id, YEAR, START_MONTH, END_MONTH, OUTPUT_DIRECTORY, id, ids)))
    print(OUTPUT_DIRECTORY)


def inspect_jsonl_files(directory, game_count):
    team_jsonl_list = os.listdir(directory)
    assert len(team_jsonl_list) == TEAM_COUNT, "Incorrect number of teams found."
    for jsonl in team_jsonl_list:
        lines = get_file_lines(os.path.join(directory, jsonl))
        # Don't assert here, just warn. Data will be cleaned up later. International opening days may cause errors here.
        if lines != game_count:
            logging.warning(f"Incorrect lines (games): {lines} != {MLB_SEASON_GAMES_COUNT} for {jsonl}")


def get_file_lines(file_path):
    with open(file_path) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


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


class TeamScheduleScraperData:
    """
    Class used to group fields used for parallel functions.
    """
    def __init__(self, id, year, start_month, end_month, output_directory):
        self.team = id
        self.year = year
        self.start_month = start_month
        self.end_month = end_month
        self.output_directory = output_directory


# class MinorLeagueScheduleScraperData(BaseScheduleScraperData):
#     def __init__(self, team, year, start_month, end_month, output_directory, id):
#         super().__init__(team, year, start_month, end_month, output_directory)
#         self.id = id


# Call scripts here TODO to a main function

# Write MLB schedules. Team names are wrapped in the function.
# execute_parallel_mlb()

# Write lists of minor league ids, if needed.
resource_levels = list(map(lambda s: s.split('_ids')[0], (filter(lambda f: '_ids.txt' in f, os.listdir(MINOR_LEAGUE_ID_PATH)))))
if set(resource_levels) != set(MINOR_LEAGUE_LEVELS):
    browser = Browser('chrome', headless=True)
    write_minor_league_team_ids(browser, MINOR_LEAGUE_ID_PATH)

# Write mlb schedules
execute_parallel_minor_league('a_adv_ids.txt')
