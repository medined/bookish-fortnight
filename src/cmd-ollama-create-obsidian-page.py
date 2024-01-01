#!/usr/bin/env python

from bs4 import BeautifulSoup
from icecream import ic
from ollama_manager import OllamaManager
from processor_generic import ProcessorGeneric
from processor_youtube import ProcessorYoutube
import re
import os


bookmark_file = "/home/medined/Documents/bookmarks_12_31_23.html"
vault_directory = '/home/medined/Dropbox/david/fences/browser-bookmarks'
recreate = False

def ellipsis(s, length=45):
    """
    Shortens a string to a specified length and adds an ellipsis if it is longer.

    Args:
    s (str): The string to shorten.
    length (int): The maximum length of the shortened string.

    Returns:
    str: The shortened string with an ellipsis if it was longer than the specified length.
    """
    if len(s) > length:
        return s[:length-3] + "..."
    else:
        return s

def sanitize_title(title):
    # Remove sequential spaces
    return re.sub(r'\s+', ' ', title)


def sanitize_filename(filename):
    
    # Remove null character and forward slash
    sanitized = re.sub(r'[\0/]', '', filename)
    
    # Optional: Remove other potentially problematic characters
    # This line removes spaces, and any character that is not alphanumeric, an underscore, or a dot.
    # You can adjust the regex pattern according to your requirements.
    sanitized = re.sub(r'[^\w.\- ]', '', sanitized)
    
    # Remove sequential spaces
    sanitized = re.sub(r'\s+', ' ', sanitized)

    return sanitized


def skippable(url):
    for x in ['docs.google', 'reddit', 'slack', 'twitter']:
        if x in url:
            return True
    return False


youtube_processor = ProcessorYoutube()
generic_processor = ProcessorGeneric()

with open(bookmark_file) as f:
    soup = BeautifulSoup(f, 'html.parser')

pages = {}
for anchor in soup.find_all('a'):
    url = anchor.get('href')
    title = sanitize_title(anchor.text)
    if url and title:
        pages[title] = url

sorted_keys = sorted(pages.keys())
page_count = len(sorted_keys)

for page_index, title in enumerate(sorted_keys):

    url = pages[title]
    
    if url.startswith('https://www.youtube.com'):
        markdown = youtube_processor.process(url)
    else:
        if skippable(url):
            print(f"{page_index}/{page_count} Processing {ellipsis(title)} - skipped")
            continue

        print(f"{page_index}/{page_count} Processing {ellipsis(title)}")
        markdown = generic_processor.process(title, url)

    if markdown is None:
        print(f"{page_index}/{page_count} Processing {ellipsis(title)} - failed - None from processor.")
        continue

    safe_filename = sanitize_filename(title)
    file_path = os.path.join(vault_directory, f"{safe_filename}.md")

    if os.path.exists(file_path) and not recreate:
        print(f"{page_index}/{page_count} {ellipsis(title)} exists")
        continue
        
    with open(file_path, "w") as f:
        f.write(markdown)
    print(f"{page_index}/{page_count} {ellipsis(title)} - created")

    # if page_index > 50:
    #     break
