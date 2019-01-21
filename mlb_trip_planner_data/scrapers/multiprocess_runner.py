import logging
import os

from multiprocessing import Pool, cpu_count
from minor_league_scraper import write_minor_league_team_ids
from utils import BaseScheduleScraperData, MinorLeagueScheduleScraperData, write_games_to_file_system


# TODO Set up a central logger with configurable level
logging.basicConfig(level=logging.INFO)
# TODO Make this command line parameters
YEAR = 2019

# CONSTANTS
TEAM_COUNT = 30
START_MONTH = 3  # Different leagues start in different months, so this could be configurable.
END_MONTH = 9
MLB_SEASON_GAMES_COUNT = 162


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

    parameter_object_list = list(map(lambda t: BaseScheduleScraperData(t, YEAR, START_MONTH, END_MONTH, OUTPUT_DIRECTORY), mlb_teams))
    assert len(parameter_object_list) == 30, "Incorrect number of teams found. Stopping execution."

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    parallel_execution(write_games_to_file_system, parameter_object_list)

    logging.info("... Finished writing schedules")
    inspect_jsonl_files(OUTPUT_DIRECTORY, MLB_SEASON_GAMES_COUNT)


def execute_parallel_minor_league(id_list_path):
    # get a list of ids
    # write_minor_league_team_ids()
    with open(os.path.join('resources', 'a_adv_ids.txt')) as f:
        data = f.readlines()
        print(data)


def inspect_jsonl_files(directory, game_count):
    team_jsonl_list = os.listdir(directory)
    assert len(team_jsonl_list) == TEAM_COUNT, "Incorrect number of teams found."
    for jsonl in team_jsonl_list:
        lines = get_file_lines(os.path.join(directory, jsonl))
        # Don't assert here, just warn. Data will be cleaned up later. International opening days may cause errors here.
        if lines != game_count:
            logging.warn(f"Incorrect lines (games): {lines} != {MLB_SEASON_GAMES_COUNT} for {jsonl}")


def get_file_lines(file_path):
    with open(file_path) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


# Call scripts here TODO to a main function
# execute_parallel_mlb()
execute_parallel_minor_league('')