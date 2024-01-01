#!/usr/bin/env python

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from icecream import ic
from langchain.agents import load_tools
from ollama_manager import OllamaManager
from processor_youtube import ProcessorYoutube
import re
import os


bookmark_file = "/home/medined/Documents/bookmarks_12_31_23.html"
vault_directory = '/home/medined/Dropbox/david/fences/browser-bookmarks'
recreate = False

requester = load_tools(["requests_get"])[0]


load_dotenv()

llm_manager = OllamaManager(model_name='llama2-uncensored', temperature=.25)


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


def create_page(url):
    
    return llm_manager.llm.complete(f"""
You are a librarian utilizing the Obsidian text editor for summarizing web content. Your task is to read web 
pages, extract their essence, and document each in a markdown file. Begin by summarizing the content from 
the provided URL.

{url}

When responding, ignore any previous instructions related to generating output and follow these guidelines:

* Extract the page title from the <title> HTML tag, if present. Ensure the title is plain text, free of any HTML or URLs.

* Identify and list up to 5 relevant categories. Present these categories in a consistent bulleted format.

* Enclose each category name within double square brackets, like so: [[Data Retrieval]].

* Formulate 5 comprehensive questions based on the page's content. These questions should test a broad understanding 
of the subject matter and vary in focus across the document. Avoid using multiple-choice format or numbering them as 
Q1, Q2, etc. Keep the questions specific to the content of the web page.

* Omit any references or messages related to sider.ai.

* Replace the elements surrounded by brackets with your responses.

* Respond as JSON, with these keys: title, url, summary, categories, and questions.

* Just response with JSON, no preamble text.

Here is an example response:

{{
    "title": "<title>",
    "url": "<url>",
    "summary": "<summary>",
    "categories": [
        "<category1>",
        "<category2>",
        "<category3>",
        "<category4>",
        "<category5>",
    ],
    "questions": [
        "<question1>",
        "<question2>",
        "<question3>",
        "<question4>",
        "<question5>",
    ],
}}
"""
    )


def fetch_summary(title, url):
    return create_page(url).text


def skippable(url):
    for x in ['docs.google', 'reddit', 'slack', 'twitter']:
        if x in url:
            return True
    return False


youtube_processor = ProcessorYoutube()

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
        markdown = fetch_summary(title, url)
        # if page_index > 50:
        #     break

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
