# Generic helper functions

import requests
import urllib.request
import os

def remove_characters(value=str, deletechars=str) -> str:
    """
    Removes the given characters from the given string.

    Parameters:
    -----------
    value: str
        String to modify
    deletechars: str
        The characters to remove
    """
    for c in deletechars:
        value = value.replace(c,'')
    return value


def download_file(url=str, output_dir=str, file_name=''):
    """
    Downloads an image given it's url. 

    Parameters:
    -----------
    url: str
        Full url to the image
    output_dir: str
        Output directory for where the image file should be saved.
    file_name: str
        Output file name for the image. 
    """
    
    # first check if output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if len(file_name) > 0:
        filename = file_name
    else:
        filename = url.split('/')[-1]

    if len(filename) == 0:
        local_path = "{0}/{1}".format(output_dir, filename)
    else:
        local_path = "{0}/{1}".format(output_dir, remove_characters(filename,'\/:*?"<>|'))
    results = requests.get(url)
    with open(local_path, 'wb') as outfile:
        outfile.write(results.content)
