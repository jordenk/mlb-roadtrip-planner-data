import logging
import os

from mlb_scraper import write_games_to_file_system
from multiprocessing import Pool, cpu_count
from utils import TeamScheduleScraperData

logging.basicConfig(level=logging.INFO)

def parallel_execution(function_arg, list_arg):
    max_processes = cpu_count() - 1
    with Pool(processes=max_processes) as pool:
        pool.map(function_arg, list_arg)


def get_file_lines(file_path):
    with open(file_path) as f:
        for i, _ in enumerate(f):
            pass
    return i + 1


def execute_parallel_mlb():
    mlb_teams = [
        "angels", "astros", "athletics", "bluejays", "braves" ,"brewers", "cardinals", "cubs", "dbacks", "dodgers",
        "giants", "indians", "mariners", "marlins", "mets", "nationals", "orioles", "phillies", "padres", "pirates",
        "rangers", "rays", "reds", "redsox", "rockies", "royals","tigers", "twins", "whitesox", "yankees"
        ]

    # TODO Make these command line parameters
    YEAR = 2019
    START_MONTH = 3 # will need to cast this command line parameter as an int 
    END_MONTH = 9 # will need to cast this command line parameter as an int 
    OUTPUT_DIRECTORY = f"raw_data/mlb/{YEAR}"
    MLB_SEASON_GAMES_COUNT = 162

    parameter_object_list = list(map(lambda t: TeamScheduleScraperData(t, YEAR, START_MONTH, END_MONTH, OUTPUT_DIRECTORY), mlb_teams))
    assert len(parameter_object_list) == 30, "Incorrect number of teams found. Stopping execution."

    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

    parallel_execution(write_games_to_file_system, parameter_object_list)

    logging.info("... Finished writing schedules") # TODO logger
    team_jsonl_list = os.listdir(OUTPUT_DIRECTORY)
    assert len(team_jsonl_list) == 30, "Incorrect number of teams found."
    for jsonl in team_jsonl_list:
        lines = get_file_lines(os.path.join(OUTPUT_DIRECTORY, jsonl))
        # Don't assert here, just warn. Data will be cleaned up later. International opening days may cause errors here.
        if lines != MLB_SEASON_GAMES_COUNT:
            logging.warn(f"Incorrect lines (games): {lines} != {MLB_SEASON_GAMES_COUNT} for {jsonl}")

# execute_parallel_mlb()