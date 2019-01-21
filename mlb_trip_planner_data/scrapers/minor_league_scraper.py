import json
import os

from bs4 import BeautifulSoup
from splinter import Browser
from utils import write_dict_list_to_file


def write_minor_league_team_data_maps(browser, output_directory="mlb_trip_planner_data/resources", link='http://www.milb.com/milb/info/affiliations.jsp'):
    """
    Scrapes milb.com to get the ids for team names. Writes data to the resources directory.
    """ 
    browser.visit(link)
    # Browser.status_code is not implemented. Use title loading as a successful load check.
    title = browser.title
    assert type(title) is str and len(title) > 0, f"Error loading page: {link}"

    aaa_teams = []
    aa_teams = []
    a_adv_teams = []
    a_teams = []
    for li in BeautifulSoup(browser.html, 'html.parser').findAll('li'):
        contents = li.contents
        if ' (AAA)' in contents:
            aaa_teams.append(get_name_and_id(contents[1]))
        elif ' (AA)' in contents:
            aa_teams.append(get_name_and_id(contents[1]))
        elif ' (A Adv.)' in contents:
            a_adv_teams.append(get_name_and_id(contents[1]))
        elif ' (A)' in contents:
            a_teams.append(get_name_and_id(contents[1]))
    write_dict_list_to_file(aaa_teams, os.path.join(output_directory, 'aaa_map.jsonl'), 'w')
    write_dict_list_to_file(aa_teams, os.path.join(output_directory, 'aa_map.jsonl'), 'w')
    write_dict_list_to_file(a_adv_teams, os.path.join(output_directory, 'a_adv_map.jsonl'), 'w')
    write_dict_list_to_file(a_teams, os.path.join(output_directory, 'a_map.jsonl'), 'w')

def get_name_and_id(tag):
    name = tag.text
    # FIXME get ids working with BS
    links = list(filter(lambda s: "http://www.milb.com/index.jsp?sid" in s, str(tag).split(" ")))
    assert len(links) == 1, "Could not parse the team id."
    return {'name': name, 'id': links[0].split("sid=")[1].rstrip('"')}


browser = Browser('chrome', headless=True)
try:
    AAA_teams = []
    write_minor_league_team_data_maps(browser)
finally:
    browser.quit()