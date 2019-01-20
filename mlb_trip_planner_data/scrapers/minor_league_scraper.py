import json

from bs4 import BeautifulSoup
from splinter import Browser
from utils import date_string_to_timestamp, get_content_list, write_dict_list_to_file

l = 'http://www.milb.com/milb/info/affiliations.jsp'

def get_team_ids(browser, link):
    """
    Scrapes milb.com to get the ids for team names.
    """
    
    browser.visit(link)
    return BeautifulSoup(browser.html, 'html.parser').findAll('li')



browser = Browser('chrome', headless=True)
try:
    data = get_team_ids(browser, l)
    for l in  data:
        if " (AAA)" in l.contents:
            print("***")
            print(l.contents)
    # print(data.prettify())
    # write_dict_list_to_file(data, 'here.jsonl')
finally:
    browser.quit()