"""
This module holds methods that all processors might need.
"""

from ollama_manager import OllamaManager
import re

class ProcessorAbstract:

    def __init__(self, model_name='solar', temperature=.25):
        self.model_name = model_name
        self.temperature = temperature
        self.llm_manager = OllamaManager(model_name=model_name, temperature=.25)
