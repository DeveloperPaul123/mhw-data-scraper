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
    if len(columns) == 3:
        # iceborn data
        name = columns[0].find('a').text
        return_monster.name = remove_characters(name, '\n').strip()
    else:
        # base mhw data
        name = columns[0].find('a').text
        return_monster.name = remove_characters(name, '\n').strip()
        img_src = row.find(class_='img-fluid')
        img_link = img_src.get('src')
        return_monster.image_link = img_link
    return return_monster

def process_monster_page(page_url=str):
    return None


url = "https://mhworld.kiranico.com/monsters"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all(class_='table table-padded')
monster_list = list()

for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        current_monster = process_monster_row(row)        
        print('{} {}'.format(current_monster.name, current_monster.image_link))