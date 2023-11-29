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
from PIL import Image
from PIL.ExifTags import TAGS

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

# All variables needed for the final file
all_phone_numbers = []
all_emails = []
all_names = []
all_links = []
all_descs = []
all_comments = []
all_scripts = []
all_tag_names = []

all_image_data = []

# For organizing all output into a single file
main_path = os.getcwd() + "\\" + "a_script_output" + "\\" + "ALL_OUTPUT.txt"


# A method to check files inside a directory
def scrape_folders():
    # Global Variables
    global white_space
    global path
    global all_phone_numbers
    global all_emails
    global all_names
    global all_links
    global all_descs
    global all_comments
    global all_scripts
    global all_tag_names

    if os.path.exists(path):
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
                    directory = os.path.join(path, files)

                    if os.path.exists(directory):
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

                    # Get Email addresses with regex
                    emails = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
                    email_addresses = re.findall(emails, html)

                    # Spit out all of the comments/scripts into a separate txt file
                    output_file_path = directory + "_output.txt"

                    # Write to files
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        # IN ORDER OF MOST IMPORTANT
                        for number in phone_numbers:
                            output_file.write(number + '\n')
                            all_phone_numbers.append(number)

                        for email_address in email_addresses:
                            output_file.write(email_address + '\n')
                            all_emails.append(email_address)

                        for name in names:
                            output_file.write(name + '\n')
                            all_names.append(name)

                        for link in links:
                            output_file.write(link['href'] + '\n')
                            all_links.append(link['href'])

                        # Description
                        output_file.write(str(description))
                        all_descs.append(str(description))

                        for comment in comments:
                            output_file.write(str(comment) + '\n')
                            all_comments.append(str(comment))

                        for script in scripts:
                            output_file.write(str(script) + '\n')
                            all_scripts.append(str(script))

                        for tag_name in tag_names:
                            output_file.write(tag_name + '\n')
                            all_tag_names.append(tag_name)

                # If it's an image file, find EXIF
                if '.jpg' in files or '.JPEG' in files or '.JPG' in files or '.png' in files or \
                        '.PNG' in files or '.gif' in files or '.bmp' in files or '.WebP' in files:

                    if 'output.txt' in files:
                        continue

                    # Change dir
                    directory = os.path.join(path, files)

                    image = Image.open(directory)
                    exifdata = image.getexif()

                    # Spit out all of the comments/scripts into a separate txt file
                    output_file_path = directory + "_output.txt"

                    # Write to files
                    with open(output_file_path, 'w', encoding='utf-8') as output_file:
                        # Get the Metadata
                        all_image_data.append("FILE: " + directory)

                        for tag_id in exifdata:
                            tag_name = TAGS.get(tag_id, tag_id)
                            value = exifdata.get(tag_id)

                            output_file.write(f"{tag_name:25}: {value}" + '\n')
                            all_image_data.append(f"{tag_name:25}: {value}" + '\n')


                if counter == amount_of_files:
                    white_space = white_space[:-5]
                    path = original_path


# Remove duplicates in the lists
def remove_duplicates(big_list):
    unique_list = []
    for item in big_list:
        if item not in unique_list:
            unique_list.append(item)

    return unique_list


# For printing files to verify directories
debug_directory = True

# DRIVER CODE
for file in local_files:
    if file == 'main.py' or file == '.idea':
        continue
    # Delete the main output file if it exists
    elif file == 'a_script_output' and os.path.exists(main_path):
        os.remove(main_path)
    else:
        if debug_directory:
            print(file)
        path = file
        original_path = path
        scrape_folders()


# Remove Duplicates
if debug_directory:
    print('Removing Duplicates!')
all_phone_numbers = remove_duplicates(all_phone_numbers)
all_emails = remove_duplicates(all_emails)
all_names = remove_duplicates(all_names)
all_links = remove_duplicates(all_links)
all_tag_names = remove_duplicates(all_tag_names)


# Sort all the output in the final file and write to it
if debug_directory:
    print('Writing to output file!')
with open(main_path, 'a', encoding='utf-8') as main_output_file:
    for numbers in all_phone_numbers:
        main_output_file.write(numbers + '\n')
    for emails in all_emails:
        main_output_file.write(emails + '\n')
    for name in all_names:
        main_output_file.write(name + '\n')
    for link in all_links:
        main_output_file.write(link + '\n')
    for description in all_descs:
        main_output_file.write(description + '\n')
    for comment in all_comments:
        main_output_file.write(comment + '\n')
    for script in all_scripts:
        main_output_file.write(script + '\n')
    for tags in all_tag_names:
        main_output_file.write(tags + '\n')
    for data in all_image_data:
        main_output_file.write(data + '\n')

if debug_directory:
    print('Done!')