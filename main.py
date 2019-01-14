import requests
import csv

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

# for t in mlb_teams:
#     print(t.url)

def main():
    data = requests.get(mlb_teams[0].url)
    link = get_home_schedule_csv_link(data)
    print(link)
    with requests.Session() as s:
        download = s.get(link+".csv")
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            print(row)

# Extract the link for the CSV home schedule.
def get_home_schedule_csv_link(requests_data):
    binary_full_schedule_string = str.encode("Download Full Season Schedule")
    for l in requests_data.iter_lines():
        if binary_full_schedule_string in l:
            soup = BeautifulSoup(str(l), 'html.parser').find_all("a")
            links = list(map(lambda s: s.get('href'), soup))
            assert len(links) == 3
            # get the home game link
            return links[1].replace("mlb.mlb.com", "www.ticketing-client.com")
    return None


main()