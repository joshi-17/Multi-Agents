from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class TriagingAgent:
    def __init__(self, model):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = model
        self.system_prompt = """You are a Triaging Agent responsible for coordinating data analysis tasks. 
        Based on user queries, you should determine which specialized agents to involve and in what order.
        Available agents are:
        - Data Processing Agent: for cleaning and preprocessing data
        - Analysis Agent: for statistical and correlation analysis
        - Visualization Agent: for creating charts and visualizations"""
        
        self.tools = [{
            "type": "function",
            "function": {
                "name": "send_query_to_agents",
                "description": "Sends the query to appropriate specialized agents",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "agents": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": ["Data Processing Agent", "Analysis Agent", "Visualization Agent"]
                            },
                            "description": "List of agents to handle the query"
                        },
                        "query": {
                            "type": "string",
                            "description": "The query to be processed"
                        }
                    },
                    "required": ["agents", "query"]
                }
            }
        }]

    def handle_query(self, user_query, conversation_messages):
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(conversation_messages)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            tools=self.tools,
            tool_choice="auto"  # Force the model to use tools
        )

        return response

# This class defines the Triaging Agent, responsible for routing user queries to the appropriate specialized agents.
# It uses the OpenAI API to determine the best agent based on the query and defined tools.
# The agent sends the query and maintains a conversation history, ensuring context is preserved across interactions. 