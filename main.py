# Garrett Maury
# 11-15-23 Web Scraper

import requests
import os
from bs4 import BeautifulSoup

# This is the local path of this python project
# The directory files should be in the same folder as main.py
local_path = '../msj scrape'
local_files = os.listdir(local_path)\

# This is for adding whitespace to visually show you are in another directory
white_space = "     "
path = ""
original_path = ""


# A method to check files inside a directory
def scrape_folders():
    global white_space
    global path

    list_of_files = os.listdir(path)
    amount_of_files = len(list_of_files)
    counter = 0
    for files in list_of_files:
        # For every file, increment the counter
        counter += 1

        print(white_space + files)
        # Use recursion to go through more directories if there are more
        if '_files' in files:
            path = path + "/" + files
            white_space += white_space
            scrape_folders()
        else:
            # Do Scraping
            if counter == amount_of_files:
                white_space = white_space[:-5]
                path = original_path


# Goes through all of the directories and checks inside them for files
for file in local_files:
    if file == 'main.py' or file == '.idea':
        continue
    else:
        print(file)
        path = file
        original_path = file
        scrape_folders()