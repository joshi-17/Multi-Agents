from openai import OpenAI
import os
from dotenv import load_dotenv
from tools.data_analysis_tools import analysis_tools

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AnalysisAgent:
    def __init__(self, model):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.system_prompt = """You are an Analysis Agent. Your role is to perform statistical, correlation, and regression analysis using the following tools:
- stat_analysis
- correlation_analysis
- regression_analysis"""
        self.tools = analysis_tools

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

# This class defines the Analysis Agent, which performs statistical, correlation, and regression analysis on data.
# It utilizes the OpenAI API along with specific analysis tools to execute the requested analyses.
# The agent processes user queries, conducts the analysis, and returns the results. 