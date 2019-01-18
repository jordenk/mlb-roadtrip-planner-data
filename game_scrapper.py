from splinter import Browser
from bs4 import BeautifulSoup


links = ['https://www.mlb.com/dodgers/schedule/2019-03']

# browser = Browser('chrome', headless=True)
# browser.visit('https://www.mlb.com/dodgers/schedule/2019-03')
# soup = BeautifulSoup(browser.html, 'html.parser')
# print(soup.prettify())

for l in links:
    print(l)
    browser = Browser('chrome', headless=True)
    browser.visit(l)
    soup = BeautifulSoup(browser.html, 'html.parser')
    print(soup.prettify())