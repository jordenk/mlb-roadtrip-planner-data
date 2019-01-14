import requests
import os

from bs4 import BeautifulSoup
from data_types.team import Team

mlb_teams = [
    Team("angels"),
    Team("astros"),
    Team("athletics"),
    Team("bluejays"),
    Team("braves"),
    Team("brewers"),
    Team("cardinals"),
    Team("cubs"),
    Team("dbacks"),
    Team("dodgers"),
    Team("giants"),
    Team("indians"),
    Team("mariners"),
    Team("marlins"),
    Team("mets"),
    Team("nationals"),
    Team("orioles"),
    Team("phillies"),
    Team("padres"),
    Team("pirates"),
    Team("rangers"),
    Team("rays"),
    Team("reds"),
    Team("redsox"),
    Team("rockies"),
    Team("royals"),
    Team("tigers"),
    Team("twins"),
    Team("whitesox"),
    Team("yankees"),
]

def main():
    # This is not concurrent since it's a pretty fast operation.
    os.makedirs("csv_data/mlb", exist_ok=True)
    os.makedirs("csv_data/aaa", exist_ok=True)
    for team in mlb_teams:
        data = requests.get(team.url)
        link = get_home_schedule_csv_link(data)
        write_csv_data_to_file(team, link, "csv_data/mlb")

# Extract the link for the CSV home schedule.
def get_home_schedule_csv_link(requests_data):
    binary_full_schedule_string = str.encode("Download Full Season Schedule")
    for l in requests_data.iter_lines():
        if binary_full_schedule_string in l:
            soup = BeautifulSoup(str(l), 'html.parser').find_all('a')
            links = list(map(lambda s: s.get('href'), soup))
            assert len(links) == 3
            # get the home game link
            return links[1].replace("mlb.mlb.com", "www.ticketing-client.com")
    return None

# Write CSV data to a file. Allow for AAA teams too. TODO Have some error handling here since this is a side effect.
def write_csv_data_to_file(team, csv_link, output_dir):
    with requests.Session() as s:
        download = s.get(csv_link)
        decoded_content = download.content.decode('utf-8')
        with open(f"{output_dir}/{team.urlName}.csv", 'w') as f:
            f.write(decoded_content)

main()