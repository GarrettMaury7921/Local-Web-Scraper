# Garrett Maury
# 11-15-23 Web Scraper

# Works on Windows

# INSTALL BEAUTIFUL SOUP, os, re, spaCy english language model
# pip install spacy
# python -m spacy download en_core_web_sm


import os
import re
import spacy
from bs4 import BeautifulSoup
from bs4 import Comment

# Load spaCy
nlp = spacy.load("en_core_web_sm")

# This is the local path of this python project
# The directory files should be in the same folder as main.py
local_path = '../msj scrape'
local_files = os.listdir(local_path)

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

        if debug_directory:
            print(white_space + files)

        # Use recursion to go through more directories if there are more
        if '_files' in files:
            path = path + "\\" + files
            white_space += white_space
            scrape_folders()
        else:
            # Do Scraping
            if '.html' in files:
                # Try not to create output.txt file for one that already exists if ran once already
                if 'output.txt' in files:
                    continue

                # Change dir
                directory = os.getcwd() + "\\" + path + "\\" + files

                with open(directory, 'r', encoding='utf-8') as file:
                    html = file.read()

                soup = BeautifulSoup(html, 'html.parser')

                # Get all text in HTML
                text = ''.join(soup.stripped_strings)

                # Get all comments / scripts / tag names / links / phone numbers
                # / people name (attempting to) in the HTML / descriptions
                comments = soup.find_all(string=lambda text: isinstance(text, Comment))
                scripts = soup.find_all('script')
                tag_names = [tag.name for tag in soup.find_all()]
                links = soup.find_all('a', href=True)
                descriptions = soup.find('meta', {'name': 'description'})
                description = descriptions.get('content') if descriptions else None
                # Common phone number formats
                phone_number_pattern = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')
                phone_numbers = re.findall(phone_number_pattern, html)
                # Get people names with spaCy
                text_processed = nlp(text)
                names = [ent.text for ent in text_processed.ents if ent.label_ == 'PERSON']

                # Spit out all of the comments/scripts into a separate txt file
                output_file_path = directory + "_output.txt"

                # Write to file
                with open(output_file_path, 'w', encoding='utf-8') as output_file:
                    # IN ORDER OF MOST IMPORTANT
                    for number in phone_numbers:
                        output_file.write(number + '\n')
                    for name in names:
                        output_file.write(name + '\n')
                    for link in links:
                        output_file.write(link['href'] + '\n')
                    # Description
                    output_file.write(str(description))
                    for comment in comments:
                        output_file.write(str(comment) + '\n')
                    for script in scripts:
                        output_file.write(str(script) + '\n')
                    for tag_name in tag_names:
                        output_file.write(tag_name + '\n')

            if counter == amount_of_files:
                white_space = white_space[:-5]
                path = original_path


# Goes through all of the directories and checks inside them for files

# For printing files to verify directories
debug_directory = False

# DRIVER CODE
for file in local_files:
    if file == 'main.py' or file == '.idea':
        continue
    else:
        if debug_directory:
            print(file)
        path = file
        original_path = path
        scrape_folders()