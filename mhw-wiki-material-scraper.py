import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv 
from common import *
import re

def process_material_row(row):
    material_data = {}
    columns = row.find_all('td')
    icon_link_element = columns[0].find('a')
    
    if(icon_link_element is None):
        print('crap row')
        return None
    icon_link = icon_link_element.get('href')

    material_data['icon_link'] = remove_characters(icon_link, '\n')

    name_raw = columns[1].text 
    name = re.sub(r'[^\x00-\x7F]','', name_raw)
    material_data['name'] = remove_characters(name, '\n').strip()
    material_data['rarity'] = remove_characters(columns[2].text, '\n').strip()
    material_data['value'] = remove_characters(columns[3].text, '\n').strip()

    return material_data

### main script area ###
### ---------------- ###
url = 'https://monsterhunter.fandom.com/wiki/MHW:_Monster_Material_List'

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all('table', class_='linetable hover')

material_items_data = list()
for table in tables:
    rows = table.find_all('tr')
    for row in rows:
        results = process_material_row(row)
        if results!= None:
            print(results)
            file_name = '{}.png'.format(results['name'].lower().replace(' ', '-'))
            download_image(str(results['icon_link']), 'images/materials', file_name)
            material_items_data.append(results)

print('Found {} total items.'.format(len(material_items_data)))
