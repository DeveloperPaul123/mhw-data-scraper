import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv 
from common import *
from collections import namedtuple
from pprint import pprint

# named tuple for monsters
monster = namedtuple('monster', 'name type image_link species description element ailments locations resistances weakness rewards')

def pretty_print_monster(mon=monster):
    pprint(dict(vars(mon)))

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
        process_monster_page(monster_link, return_monster)

    return return_monster

def process_monster_page(page_url=str, mon=monster):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")

    project_info = soup.find(class_='project-info')
    description = project_info.find(class_='col-sm-6').text
    
    mon.description = remove_characters(description, '\n').strip()

    balance_table = project_info.find(class_='balance-table')

    # find all columns in the balance table
    balance_table_rows = balance_table.find_all('td')

    # set the species
    mon.species = remove_characters(balance_table_rows[0].text, '\n').strip()

    return


#--script area--#

# base url to download data from
url = "https://mhworld.kiranico.com/monsters"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# data is organized in tables on the website
tables = soup.find_all(class_='table table-padded')
monster_list = list()

# change to True to download thumbnail images (where available) for the monsters.
download_images = True
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        current_monster = process_monster_row(row)        
        print('{} {} {}'.format(current_monster.name, current_monster.species, current_monster.image_link))
        if download_images and current_monster.image_link is not None:
            # download the thumbnail images for the monsters (from common.py)
            download_file(current_monster.image_link, 
                'images/monsters/textured', 
                '{}.png'.format(str(current_monster.name).lower().replace(' ', '-')))
            