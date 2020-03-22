import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv
from common import *
from collections import namedtuple
from pprint import pprint
from requests_html import HTMLSession
import re

monster = namedtuple("monster", "name type species description")
monster_reward = namedtuple(
    "monster_reward", "monster_name item_name droprate rank condition stack"
)

# --script area--#

# base url to download data from
base_url = "https://mhw.poedb.tw"
url = "{}/eng/monsters/large".format(base_url)

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


cards = soup.find_all(class_="card")
monsters_list = list()
monster_reward_list = list()
session = HTMLSession()

for card in cards:
    if any(x in card.div.text for x in ["Relict, Wyvern", "Dragon", "Beast"]):
        # monster species
        monster_species = card.div.text
        print(card.div.text)

        link_elements = card.find_all("a")
        for element in link_elements:
            monster_name = element.text
            
            print(monster_name)
            link = element.get("href")
            print(link)
            monster_link = "{}{}".format(base_url, link)

            mon_page_response = None
            max_attempts = 6
            attempt = 0
            while mon_page_response is None and attempt <= max_attempts:
                try:
                    attempt = attempt + 1
                    mon_page_response = session.get(monster_link)
                except:
                    print('Unable to load page, trying again')
                    time.sleep(1.0)
            
            mon_page_response.html.render(retries = 20, timeout= 30.0, wait=2.0)
            monster_soup = BeautifulSoup(mon_page_response.html.raw_html, "html.parser")

            monster_page_cards = monster_soup.find_all(class_="card")
            for mon_card in monster_page_cards:
                mon_card_title = mon_card.div.text
                # TODO: Get monster info and add to list
                if "Reward" in mon_card.div.text:
                    print("Parsing reward table...")
                    monster_rank = mon_card_title.split(" ")[1].strip()
                    reward_rows = mon_card.find_all("tr")
                    for reward in reward_rows:
                        reward_columns = reward.find_all("td")
                        if len(reward_columns) != 3:
                            # Skip reward rows that don't have enough columns
                            continue
                        reward_condition = reward_columns[0].text
                        reward_item_raw = reward_columns[1].text
                        # some reward changes are of the form: 1% (Guaranteed)
                        # so we remove it here
                        reward_chance = reward_columns[2].text.replace("(Guaranteed)", "").strip()
                        matcher = re.compile("\d+")
                        if matcher.search(reward_item_raw):
                            item_parts = reward_item_raw.rpartition(" ")
                            reward_item = item_parts[0].strip()
                            reward_stack = int(
                                remove_characters(item_parts[2], "x\n").strip()
                            )
                            mon_reward = monster_reward(
                                monster_name,
                                reward_item,
                                reward_chance,
                                monster_rank,
                                reward_condition,
                                reward_stack,
                            )
                            monster_reward_list.append(mon_reward)

# dump the reward list
# first check if output dir exists, create it if it doesn't
if not os.path.exists('scraped_data'):
    os.mkdir('scraped_data')

# TODO: Open CSV file for monster data and dump it here

# open CSV file and dump rewards
with open('scraped_data/monster_rewards.csv', 'w', newline='\n') as csv_file:
    reward_writer = csv.writer(csv_file, delimiter=',')
    print("Exporing rewards list to CSV file...")
    print("Total rewards: {}".format(len(monster_reward_list)))
    for reward in monster_reward_list:
        reward_writer.writerow(
            [
                reward.monster_name,
                reward.condition,
                reward.rank,
                reward.item_name,
                reward.stack,
                int(remove_characters(reward.droprate, '%').strip())
            ]
        )
