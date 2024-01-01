#!/usr/bin/env python

import re
from bs4 import BeautifulSoup

bookmark_file = "/home/medined/Documents/bookmarks_12_31_23.html"

with open(bookmark_file) as f:
    soup = BeautifulSoup(f, 'html.parser')

for anchor in soup.find_all('a'):
    url = anchor.get('href')
    title = anchor.text
    if url and title:
        print(f"{title}: {url}")
