from bs4 import BeautifulSoup
from splinter import Browser
from utils import get_content_list

links = ['https://www.mlb.com/dodgers/schedule/2019-04']


def get_mlb_games(browser, link):
    browser.visit(link)
    # soup = BeautifulSoup(browser.html, 'html.parser').find('body').find_all('.regular-season')
    date_rows = BeautifulSoup(browser.html, 'html.parser').findAll('td', {'class': 'regular-season'})
    for row in date_rows:
        is_home_game = 'home' in row.attrs.get('class')
        day = row.find('div', {'class': 'day-of-month-label'}).contents[0]
        month = '3'
        year = '2019'

        opponent_names = get_content_list(row.find_all('div', {'class': 'opponent-name'}))
        opponent_tri_codes = get_content_list(row.find_all('div', {'class': 'opponent-tricode'}))
        primary_times = get_content_list(row.find_all('div', {'class': 'primary-time'}))

        for name, code, time in zip(opponent_names, opponent_tri_codes, primary_times):
            print(name, code, time, is_home_game)
        # print(f"{day} {opponent_names} {opponent_tri_codes} {primary_times}")


def write_to_file(data, path):
    print(data)
    with open(path, 'w') as f:
        for d in data:
            print("-------")
            # print(d)
            n = d.find('div', {'class': 'opponent-name'})
            print(n)
            #f.write(d)

browser = Browser('chrome', headless=True)
get_mlb_games(browser, links[0])
browser.quit()


# write_to_file(data, 'test_data')