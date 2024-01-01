"""
This module generates markdown that describes a YouTube video. The markdown is 
intended to be used as an Obsidian note.

The key steps are:

* Load YouTube transcript and metadata
* Construct prompt to summarize and categorize
* Query LLM manager
* Handle invalid JSON responses
* Extract summary and categories
* Generate Markdown output
"""

from langchain.document_loaders import YoutubeLoader
from ollama_manager import OllamaManager
from processor_abstract import ProcessorAbstract
import json

class ProcessorYoutube(ProcessorAbstract):

    def __init__(self, model_name='solar', temperature=.25):
        super().__init__(model_name, temperature)

    def process(self, youtube_url):

        loader = None
        try:
            loader = YoutubeLoader.from_youtube_url(youtube_url, add_video_info=True)
        except ValueError as e:
            print(f"{youtube_url} - {e}")
            return None 
        
        content = loader.load()[0].page_content

        author = loader._get_video_info()['author']
        description = loader._get_video_info()['description']
        length = loader._get_video_info()['length']
        publish_date = loader._get_video_info()['publish_date']
        thumbnail_url = loader._get_video_info()['thumbnail_url']
        title = loader._get_video_info()['title']
        view_count = loader._get_video_info()['view_count']

        query = f"""
You are a librarian utilizing the Obsidian text editor for summarizing web content. Your task is to 
summarize and categorize youtube transcripts. The context starts now and finishes with "END END END" 
on a single line. This work is very important for the education of young people. Please do your best. Take
your time. The context is as follows:

{content}

END END END
    
When responding, ignore any previous instructions related to generating output and follow these guidelines:
    
* Summarize the transcript for 9th grade students. The summary should be 3-5 sentences.
* Identify and list up to 5 relevant categories.

Format the response in JSON, with keys for 'summary' and 'categories."

Here is an example response:

{{
    "summary": "<summary>",
    "categories": [
        "<category1>",
        "<category2>",
        "<category3>",
        "<category4>",
        "<category5>",
    ]
}}

        """

        attempts = 0        
        while True:
            if attempts > 5:
                print(f"Too many attempts. The LLM is not creating valid JSON for {youtube_url}. The last response was:\n{response_json}")
                return None

            #
            # Sometimes the LLM does not generate valid JSON. If that happens, try again.
            #
            response_json = None
            response_text = None
            try:
                response = self.llm_manager.llm.complete(query)
                response_text = response.text
                if response_text is None:
                    print(attempts, youtube_url, "Empty response.")
                    return None
                response_json = json.loads(response_text)
            except json.decoder.JSONDecodeError:
                print(f"JSON Parse exception: {attempts}, {youtube_url}, {response_text}")
                attempts += 1
                continue

            break
        
        summary = response_json['summary']
        categories = response_json['categories']

        markdown = f"""
# Title
{title}

# YouTube URL
{youtube_url}

# Thumbnail URL
<img src="{thumbnail_url}" width="300">

# Summary
{summary}

# Categories
"""

        for category in categories:
            markdown += f"""* [[{category}]]\n"""

        markdown += f"""
# Description
{description}

# Author
{author}

# Length
{length}

# Publication Date
{publish_date}

# View Count
{view_count:,}
"""

        return markdown
