import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import csv 

def remove(value, deletechars):
    for c in deletechars:
        value = value.replace(c,'')
    return value

def download_image(url=str, output_dir=str, file_name=''):
    filename = url.split('/')[-1]
    if len(filename) == 0:
        local_path = "{0}/{1}".format(output_dir, filename)
    else:
        local_path = "{0}/{1}".format(output_dir, remove(file_name,'\/:*?"<>|'))
    results = requests.get(url)
    with open(local_path, 'wb') as outfile:
        outfile.write(results.content)

### main script ###

number_of_weapons = 14
url = 'https://mhworld.kiranico.com/weapons'
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

element_headers = soup.find_all(class_='element-header')
for header in element_headers:
    print(header)

rows = soup.findAll('tr')
download_files = False

with open('data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"')
    for row in rows:

        img_src = row.find(class_='img-fluid')
        name = row.find(class_='d-none d-xl-inline-block')
        info_columns = row.find(class_='text-center')

        if info_columns != None:
            for column in info_columns:
                if column.find('ruby') != -1 and column.find('rt') != -1:
                    bloated_attack = column.next_element
                    raw_attack = column.find('rt')
                    if bloated_attack != None and raw_attack != None and name != None:
                        print("{} | {} | {}".format(name.find('a').text, bloated_attack, raw_attack.text))

                        if img_src != None and download_files:
                            img_link = img_src.get('src')
                            download_image(img_link, 'thumbs', "{}.png".format(name.find('a').text))
                        csv_writer.writerow([name.find('a').text, bloated_attack, raw_attack.text])
                        csv_file.flush()
