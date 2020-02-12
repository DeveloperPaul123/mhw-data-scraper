import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv 
from common import *
from collections import namedtuple
from pprint import pprint
from selenium import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys

monster = namedtuple('monster', 'name type image_link species description element ailments locations resistances weakness rewards')

def pretty_print_monster(mon=monster):
    pprint(dict(vars(mon)))

# base url to download data from
url = "https://monsterhunterworld.wiki.fextralife.com/Monsters"


browser = Chrome(ChromeDriverManager().install())
browser.get(url)

heights = []
counter = 0
for i in range(1,300):
    bg = browser.find_element_by_css_selector('body')
    time.sleep(0.5)
    bg.send_keys(Keys.PAGE_DOWN)
    heights.append(browser.execute_script("return document.body.scrollHeight"))
    try :
        bottom = heights[i-16]
    except:
        pass
    if i%16 ==0:
        new_bottom = heights[i-1]
        if bottom == new_bottom:
            break

response = requests.get(url)
soup = BeautifulSoup(browser.page_source, "html.parser")

# change to True to download thumbnail images (where available) for the monsters.
download_images = True

monster_rows = soup.find_all('div', class_='row')

print(len(monster_rows))
for monster in monster_rows:
    columns = monster.find_all('div', class_='col-sm-4')
    for column in columns:
        images = column.find_all('img')
        if(len(images) == 0):
            print('No images for {}'.format(column))
        for img in images:
            # download the image
            img_url = str(img.get('src'))
            if 'png' in img_url and 'icon' in img_url:
                base_image_url = 'https://monsterhunterworld.wiki.fextralife.com'
                download_url = "{0}{1}".format(base_image_url, img_url)
                print(download_url)
                download_file(download_url, 
                    'images/monsters')
    