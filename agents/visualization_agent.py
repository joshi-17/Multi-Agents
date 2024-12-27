from openai import OpenAI
import os
from dotenv import load_dotenv
from tools.data_visualization_tools import visualization_tools

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class VisualizationAgent:
    def __init__(self, model):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.system_prompt = """You are a Visualization Agent. Your role is to create bar charts, line charts, and pie charts using the following tools:
- create_bar_chart
- create_line_chart
- create_pie_chart"""
        self.tools = visualization_tools

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

# This class defines the Visualization Agent, responsible for creating various types of charts (bar, line, pie) from data.
# It uses the OpenAI API and a set of visualization tools to generate the requested charts.
# The agent receives a query, creates the visualization, and returns the chart data. 