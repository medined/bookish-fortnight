#!/usr/bin/env python

from dotenv import load_dotenv
from langchain.agents import load_tools
from langchain.utilities import TextRequestsWrapper
from icecream import ic

bookmark_file = "/home/medined/Documents/bookmarks_12_31_23.html"

vault_directory = '/home/medined/Dropbox/david/fences/browser-bookmarks'
url = "https://blog.llamaindex.ai/boosting-rag-picking-the-best-embedding-reranker-models-42d079022e83"
recreate = False


requester = load_tools(["requests_get"])[0]

requests = TextRequestsWrapper()
content = requests.get(url)

from openai import OpenAI
import openai
import os
import requests

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def create_page(content):
    
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""
You are a librarian who uses the Obsidan text editor. You read web pages, then summarize and create a markdown file for each page. Summarize the content found at the URL given below. 

{url}

Respond in the FORMAT below. Follow these rules:

* Select up to 5 appropriate categories to include in the page's front matter. Display the categories using a comma-delimited list.
* Surround each category with double square brackets. For example, [[Data Retrieval]]
* Generate 5 questions that can be used to text overall knowledge of the subject matter in the page. The questions should be diverse in nature across the document. The questions should not contain options, not start with Q1/ Q2. Restrict the questions to the web poage content.
* Don't display a message about sider.ai. 
* Display your response as YAML.

FORMAT

[PAGE_TITLE]

# URL
[URL]

# Categories
[CATEGORIES]

# Summary
[SUMMARY]

# Questions
[QUESTIONS]
"""
            }
        ],
        model="gpt-3.5-turbo",
    )
  
response = create_page(content)

message = str(response.choices[0].message.content) if response.choices else None

if message:
    lines = message.split("\n")
    title = lines[0]
    content = lines[1:]

    title = title.strip()
    title = title.replace("&amp;", " and ")
    title = title.replace(":", " -")

    if title.startswith('['):
        title = title[1:]

    if title.endswith(']'):
        title = title[:-1]

        
    file_path = os.path.join(vault_directory, f"{title}.md")

    create_file_flag = True

    if os.path.exists(file_path) and not recreate:
        create_file_flag = False
        print(f"{file_path}: exists, therefore skipped.")
        
    if create_file_flag:
        with open(file_path, "w") as f:
            f.write("\n".join(content))
        print(f"{file_path}: created")
