import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv 
from common import *
from collections import namedtuple

event = namedtuple('event', 'title image_link rank')
def duplicates_with_count(elements):
    dict_of_elements = dict()
    for item in elements:
        if item['name'] in dict_of_elements:
            dict_of_elements[item['name']] +=1
        else:
            dict_of_elements[item['name']] = 1

    dict_of_elements = { key:value for key, value in dict_of_elements.items() if value > 1}

    return dict_of_elements

def process_event_row(value, event_rank = str) -> event:
    image = value.find(class_='image')
    image_url = None
    if image is not None:
        image_url = image.find('img').get('src')
    
    quest_title = value.find(class_='title')
    if(quest_title is not None and image_url is not None):
        evt = event
        evt.title = remove_characters(quest_title.text, '\n').strip()
        evt.image_link = image_url
        evt.rank = event_rank
        return evt
    return None

urls = {"http://game.capcom.com/world/us/schedule.html", "http://game.capcom.com/world/us/schedule-master.html"}
ranks = {"Low/High", "Master"}
total_events = 0

# get all events from the API
api_url = 'https://mhw-db.com/events'
api_response = requests.get(api_url)
api_json = api_response.json()

# change this to false to avoid downloading the images
download_images = True
longest_title = ''
for url, rank in zip(urls, ranks):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    tables = soup.find_all('tbody')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            event_row = process_event_row(row, rank)
            if(event_row is not None):
                total_events +=1
                if len(event_row.title) > len(longest_title): 
                    longest_title = event_row.title
                print('{} {} {}'.format(event_row.title, event_row.rank, event_row.image_link))
                # find the id
                event_id = -1
                for item in api_json:
                    if item['name'] == event_row.title:
                        event_id = item['id']
                        if download_images:
                            download_file(event_row.image_link, 
                                'images/events', '{}.png'.format(event_id))

print('Total events found: {}'.format(total_events)) 
print('Longest Title: {}'.format(longest_title))