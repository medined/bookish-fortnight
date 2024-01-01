
from llama_index.llms import Ollama
from llama_index import (
    set_global_service_context,
    ServiceContext,
)

class OllamaManager:
    
    def __init__(self, model_name="llama2", temperature=.50):
        self.model_name = model_name
        self.llm = Ollama(
            model=self.model_name,
            temperature=temperature,
        )
        self.service_context = ServiceContext.from_defaults(
            embed_model="local",
            llm=self.llm,
        )        
        set_global_service_context(self.service_context)
