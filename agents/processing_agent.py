from openai import OpenAI
import os
from dotenv import load_dotenv
from tools.data_processing_tools import preprocess_tools

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class ProcessingAgent:
    def __init__(self, model):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.system_prompt = """You are a Data Processing Agent. Your role is to clean, transform, and aggregate data using the following tools:
- clean_data
- transform_data
- aggregate_data"""
        self.tools = preprocess_tools

    def handle_query(self, query):
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.append({"role": "user", "content": query})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            tools=self.tools,
        )

        return response

# This class defines the Data Processing Agent, which handles data cleaning, transformation, and aggregation tasks.
# It uses the OpenAI API and a set of predefined tools to perform these operations on the provided data.
# The agent receives a query, processes it using the appropriate tools, and returns the processed data. 