import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv 
from common import *
from collections import namedtuple
from pprint import pprint
from requests_html import HTMLSession
import re # regular expressions

# named tuple for monsters
monster = namedtuple('monster', 'name type image_link species description element ailments locations resistances weakness rewards')
monster_reward = namedtuple('monster_reward', 'name droprate rank condition stack')

def pretty_print_monster(mon=monster):
    pprint(dict(vars(mon)))

def pretty_print_monster_reward(reward=monster_reward):
    print("{} {} {} {}".format(reward.name, reward.droprate, reward.rank, reward.condition))

def contains_number(s):
    return any(s.isdigit() for i in s)

def process_monster_row(row, monster_type=str) -> monster:
    return_monster = monster
    columns = row.find_all('td')
    name = columns[0].find('a').text
    monster_link = columns[0].find('a').get('href')

    if len(columns) == 3:
        # iceborn data
        return_monster.name = remove_characters(name, '\n').strip()
        return_monster.image_link = None
    else:
        # base mhw data
        return_monster.name = remove_characters(name, '\n').strip()
        img_src = row.find(class_='img-fluid')
        img_link = img_src.get('src')
        return_monster.image_link = img_link

    if monster_link is not None:
        return_monster = process_monster_page(monster_link, return_monster)

    return return_monster

def process_monster_page(page_url=str, mon=monster):
    session = HTMLSession()
    response = session.get(page_url)
    response.html.render()

    soup = BeautifulSoup(response.html.raw_html, "html.parser")

    project_info = soup.find(class_='project-info')
    description = project_info.find(class_='col-sm-6').text
    
    mon.description = remove_characters(description, '\n').strip()

    balance_table = project_info.find(class_='balance-table')

    # find all columns in the balance table
    balance_table_rows = balance_table.find_all('td')

    # set the species
    mon.species = remove_characters(balance_table_rows[0].text, '\n').strip()
    # initialize the list
    mon.rewards = list()

    # find all element wrappers
    element_wrappers = soup.find_all(class_='element-wrapper')
    for wrapper in element_wrappers:
        header = wrapper.find(class_='element-header')
        contents = wrapper.find(class_='row')
        if header != None:
            header_text = remove_characters(header.text, '\n').strip().lower()
            print('header: {}'.format(header_text))
            if header_text == 'carves' or header_text == 'rewards' or header_text == 'investigations':
                # get the rank columns
                rank_columns = contents.find_all(class_='col-lg-4')
                for rank_column in rank_columns:
                    rank = remove_characters(rank_column.find('h6').text, '\n').strip().lower()
                    # print("rank: {}".format(rank))                   
                    if rank == 'master rank' or rank == 'high rank' or rank == 'low rank':
                        tables = rank_column.find_all('table')
                        for table in tables:
                            if table == None:
                                continue
                            rows = table.find_all('tr')
                            reward_condition = None
                            for row in rows:
                                columns = row.find_all('td')
                                if len(columns) == 1:
                                    # title column
                                    column_title = remove_characters(columns[0].text, '\n').strip()
                                    print("column title: {}".format(column_title))
                                    reward_condition = column_title
                                elif reward_condition != None:
                                    reward_text = row.text.strip()
                                    print("reward text: {}".format(reward_text))
                                    # rpartition always returns 3 parts, first, delimeter and the second part
                                    parts = reward_text.rpartition(' ')
                                    name = parts[0]
                                    # sometimes the name contains the quantity so we need to parse this
                                    # first set default
                                    stack = 1
                                    matcher = re.compile('\d+')
                                    if matcher.search(name):
                                        # name contains quantity so we need to parse it
                                        # quanity is at the end, example: Hard Odogaron Sinew x3
                                        name_parts = name.rpartition(' ')
                                        # update the name to not include the `x2` or whatever
                                        name = name_parts[0]
                                        stack = int(remove_characters(name_parts[2], 'x\n').strip())
                                    droprate = parts[2]

                                    # process the reward_condition
                                    if "{}'s".format(mon.name) in reward_condition:
                                        reward_condition = reward_condition.replace(" {}'s".format(mon.name), "")
                                    elif mon.name in reward_condition:
                                        reward_condition = reward_condition.replace(" {}".format(mon.name), "")

                                    reward = monster_reward(parts[0], parts[2], rank, reward_condition.strip(), stack)
                                    pretty_print_monster_reward(reward)
                                    mon.rewards.append(reward)

    return mon

def process_ranked_column_rewards(rank_column, rank) -> list():
    tables = rank_column.find_all(class_='table-responsive')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            columns = row.find_all('td')
            if len(columns) == 1:
                # title column
                print(columns[0].text)
    return

def to_rank_short_name(rank_name=str):
    parts = rank_name.split(' ')
    return '{}{}'.format(parts[0][0].upper(), parts[1][0].upper())

#--script area--#

# base url to download data from
url = "https://mhworld.kiranico.com/monsters"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# data is organized in tables on the website
tables = soup.find_all(class_='table table-padded')
monster_list = list()

# change to True to download thumbnail images (where available) for the monsters.
download_images = False
with open('scraped_data/monster_rewards.csv', 'w', newline='\n') as csv_file:
    reward_writer = csv.writer(csv_file, delimiter=',')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            current_monster = process_monster_row(row)        
            monster_list.append(current_monster)
            print('{} {} {}'.format(current_monster.name, current_monster.species, current_monster.image_link))
            for reward in current_monster.rewards:
                reward_writer.writerow(
                    [
                        monster.name, 
                        reward.condition, 
                        to_rank_short_name(reward.rank), 
                        reward.name, 
                        reward.stack, 
                        int(remove_characters(reward.droprate.strip(), '\n%'))
                    ]
                )
                print("{} {} {} {} {}".format(reward.name, reward.rank, reward.condition, reward.droprate, reward.stack))
            if download_images and current_monster.image_link is not None:
                # download the thumbnail images for the monsters (from common.py)
                download_file(current_monster.image_link, 
                    'images/monsters/textured', 
                    '{}.png'.format(str(current_monster.name).lower().replace(' ', '-')))        
