import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv 
from common import *
from collections import namedtuple
from pprint import pprint
from requests_html import HTMLSession

monster = namedtuple('monster', 'name type species description')
monster_reward = namedtuple('monster_reward', 'monster_name item_name droprate rank condition stack')

#--script area--#

# base url to download data from
base_url = "https://mhw.poedb.tw"
url = "{}/eng/monsters/large".format(base_url)

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


cards = soup.find_all(class_="card")
monsters = list()
session = HTMLSession()

for card in cards:
    if any(x in card.div.text for x in ['Wyvern', 'Dragon', 'Beast']):
        # monster species
        monster_species = card.div.text
        print(card.div.text)

        link_elements = card.find_all('a')
        for element in link_elements:
            link = element.get('href')
            print(link)
            monster_link = '{}{}'.format(base_url,link)

            mon_page_response = session.get(monster_link)
            mon_page_response.html.render()
            monster_soup = BeautifulSoup(mon_page_response.html.raw_html, "html.parser")

            monster_page_cards = monster_soup.find_all(class_="card")
            for mon_card in monster_page_cards:
                if "Reward" in mon_card.div.text:
                    print("Found reward table parsing...")

                    reward_rows = mon_card.find_all('tr')
                    for reward in reward_rows:
                        reward_columns = reward.find_all('td')
                        if len(reward_columns) != 3: 
                            continue
                        print('{} {} {}'.format(reward_columns[0].text, reward_columns[1].text, reward_columns[2].text))
        

