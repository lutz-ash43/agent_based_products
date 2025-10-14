from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model
import os

class LLMManager:
    def __init__(self):
        # Define llm db and tools 
        if not os.environ.get("GOOGLE_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = 'AIzaSyCBV903MIqJH6pMAxuY0iCC4xjF5Pn1TZw'
        self.llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

    def invoke(self, prompt: ChatPromptTemplate, **kwargs) -> str:
        messages = prompt.format_messages(**kwargs)
        response = self.llm.invoke(messages)
        return response.content