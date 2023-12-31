#!/usr/bin/env python

from icecream import ic
from ollama_manager import OllamaManager
from processor_youtube import ProcessorYoutube

def main():
    youtube_url = "https://www.youtube.com/watch?v=yRwFgZSiDUc"
    youtube_url = "https://www.youtube.com/watch?v=dq1Sjb8IGow"
    processor = ProcessorYoutube()
    response = processor.process(youtube_url)
    print(response)
    
if __name__ == "__main__":
    main()
