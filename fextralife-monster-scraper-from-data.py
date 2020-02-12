import csv
from common import *
import requests
from image_utils import resize_image
import os

output_bb_size = 400
output_image_size = 512

with open('data/monsters/monster_base.csv', 'r') as csvfile:
    monster_reader = csv.reader(csvfile, delimiter=',')
    title_row = True
    for row in monster_reader:
        if title_row:
            title_row = False
            continue

        base_url = "https://monsterhunterworld.wiki.fextralife.com/file/Monster-Hunter-World/gthumbnails/mhw"
        base_url_alt = "https://monsterhunterworld.wiki.fextralife.com/file/Monster-Hunter-World/gthumbnails/MHW"
        alt_base_url = "https://monsterhunterworld.wiki.fextralife.com/file/Monster-Hunter-World/mhw"
        monster_id = int(row[0])
        
        image_name_base = ''
        if monster_id > 100:
            image_name_base = image_name_base + 'i-'
        else:
            image_name_base = image_name_base +'-'
        
        monster_name = str(row[1])
        image_file_name = "{}_icon".format(monster_name.lower().replace(' ', '_'))
        image_file_name_alt = "{}_Icon".format(monster_name.replace(' ', '_'))
        image_file_name_alt2 = "icono_{}".format(monster_name.lower().replace(' ', '_'))

        image_name = image_name_base + image_file_name
        image_name_alt = image_name_base + image_file_name_alt
        image_name_alt2 = image_name_base + image_file_name_alt2
        urls = list()
        urls.append(base_url + image_name + ".png")
        urls.append(base_url_alt + image_name_alt + ".png")
        urls.append(base_url + image_name_alt2 + ".png")
        urls.append(base_url+ image_name + '2.png')
        urls.append(alt_base_url + image_name + ".png")

        downloaded = False
        for url in urls:
            response = requests.get(url)
            if response.ok and not downloaded:
                downloaded = True
                # print('Downloading {}'.format(url))
                download_directory = 'images/monsters'
                output_directory = 'images/monsters/rescaled'
                if not os.path.exists(output_directory):
                    os.makedirs(output_directory)
                output_file_name = '{}.png'.format(str(monster_name.lower().replace(' ', '-')))
                download_file(
                    url, 
                    'images/monsters',
                    output_file_name)

                resize_image('{}/{}'.format(download_directory, output_file_name),
                    '{}/{}'.format(output_directory, output_file_name),
                    output_bb_size, 
                    output_image_size)

                break
            # else: 
                # print('Url failed {}'.format(url))

        if not downloaded:
            print("{} no download".format(monster_name))