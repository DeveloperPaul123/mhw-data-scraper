import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv 
from common import *

def process_weapon_page(page_url=str):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, "html.parser")
    project_info = soup.find(class_='project-info')
    description = project_info.find(class_ = 'col-sm-6')

    data_table = project_info.find(class_='balance-table')
    cells = data_table.find_all('td')
    weapon_data = {}
    for cell in cells:
        label = cell.find(class_='balance-label smaller lighter text-nowrap')
        if label != None:
            value = cell.find('strong')
            if value != None:
                value_text = value.text
                label_value = label.text.lower().strip()
                if label_value == 'attack':
                    attack, true_raw = value_text.split('|')
                    weapon_data['attack'] = int(attack.strip())
                    weapon_data['true_raw'] = int(true_raw.strip())
                elif label_value == 'rarity':
                    weapon_data[label_value] = int(value_text.replace('Rarity', ''))
                elif label_value == 'affinity':
                    weapon_data[label_value] = int(value_text.replace('%', ''))
                elif label_value == 'element':
                    # split element type and amount
                    element_string = value_text.lower()
                    weapon_data['element_hidden'] = False
                    weapon_data['element_type'] = ''
                    weapon_data['element_amount'] = 0
                    if len(element_string) > 4:
                        if value_text.find('(') != -1:
                            weapon_data['element_hidden'] = True                           

                        split_location = -1
                        process_string = remove_characters(element_string, '()\n').replace(' ', '').strip()
                        for i, c in enumerate(process_string):
                            if c.isdigit():
                                split_location = i
                                break
                        if split_location > 0:
                            element_type = process_string[0:split_location]
                            element_amount = int(process_string[split_location+1:])
                            weapon_data['element_type'] = element_type
                            weapon_data['element_amount'] = element_amount
                else:
                    weapon_data[label_value] = value_text.strip().replace('\n', '').replace(' ', '')

    return weapon_data


def process_weapon_row(value, weapon_type=str):
    use_type = weapon_type.replace(' ', '-').lower()
    img_src = row.find(class_='img-fluid')
    name = row.find(class_='d-none d-xl-inline-block')
    
    if name != None:
        weapon_link = name.find('a').get('href')
        print("Weapon link: {}".format(weapon_link))

        return process_weapon_page(weapon_link)
    
    return None

    # WIP
    # TODO: Take into account rows that don't have a link (i.e. MR weapons from IB)
    info_columns = row.find(class_='text-center')

    if info_columns != None:
        for column in info_columns:
            if column.find('ruby') != -1 and column.find('rt') != -1:
                bloated_attack = column.next_element
                raw_attack = column.find('rt')
                if bloated_attack != None and raw_attack != None and name != None:
                    print("{} | {} | {}".format(name.find('a').text, bloated_attack, raw_attack.text))
                    
                    if img_src != None:
                        img_link = img_src.get('src')
                        return {
                            'id': -1,
                            'image_link' : img_link, 
                            'name': name.find('a').text, 
                            'attack' : bloated_attack, 
                            'true_raw':raw_attack.text,
                            'weapon_type': use_type
                            }

### main script area ###
### ---------------- ###
number_of_weapons = 14
url = 'https://mhworld.kiranico.com/weapons'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all(role='tabpanel')

table_columns = ['id','name_en', 'weapon_type', 'previous_en', 'category', 'rarity', 'attack', 'affinity', 'defense', 'element_hidden', 'element1', 'element1_attack', 'element2', 'element2_attack', 'elderseal', 'slot_1', 'slot_2', 'slot_3' ,'kinsect_bonus' ,'phial' ,'phial_power', 'shelling', 'shelling_level', 'notes', 'ammo_config', 'skill']

for table in tables:
    element_header = table.find(class_='element-header')
    weapon_type = element_header.text
    print(weapon_type)
    rows = table.find_all('tr')
    for row in rows:
        results = process_weapon_row(row, weapon_type)
        if results != None:
            print(results)
