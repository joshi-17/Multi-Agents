# This file handles the execution of tools and the overall flow of user messages in the multi-agent system.
# The `execute_tool` function executes specific tools based on the agent's response, while `handle_user_message` manages the conversation flow.
# It interacts with the triaging agent and other specialized agents to process user queries and maintain conversation history. 

import json
from agents.processing_agent import ProcessingAgent
from agents.analysis_agent import AnalysisAgent
from agents.visualization_agent import VisualizationAgent
from tools.data_processing_tools import clean_data, transform_data, aggregate_data
from tools.data_analysis_tools import stat_analysis, correlation_analysis, regression_analysis
from tools.data_visualization_tools import create_bar_chart, create_line_chart, create_pie_chart
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

OPENAI_MODEL = os.getenv("OPENAI_MODEL")

def execute_tool(tool_calls, conversation_messages):
    if not tool_calls:
        return
        
    for tool_call in tool_calls:
        try:
            tool_name = tool_call.function.name
            tool_arguments = json.loads(tool_call.function.arguments)
            
            if tool_name == 'clean_data':
                df = pd.DataFrame([row.split(',') for row in tool_arguments['data'].strip().split('\n')[1:]], 
                                columns=[col.strip() for col in tool_arguments['data'].split('\n')[0].split(',')])
                # Remove duplicates
                df = df.drop_duplicates()
                # Handle missing values
                df = df.replace('null', pd.NA)
                cleaned_data = df.to_dict(orient='records')
                conversation_messages.append({
                    "name": tool_name,
                    "content": json.dumps({"cleaned_data": cleaned_data})
                })
            
            elif tool_name == 'stat_analysis':
                df = pd.DataFrame(json.loads(tool_arguments['data']))
                stats = {}
                for column in df.columns:
                    if column != 'date':  # Skip date column for statistics
                        stats[column] = {
                            'mean': df[column].astype(float).mean(),
                            'median': df[column].astype(float).median(),
                            'std': df[column].astype(float).std(),
                            'min': df[column].astype(float).min(),
                            'max': df[column].astype(float).max()
                        }
                conversation_messages.append({
                    "name": tool_name,
                    "content": json.dumps({"stats": json.dumps(stats)})
                })
            
            elif tool_name == 'correlation_analysis':
                df = pd.DataFrame(json.loads(tool_arguments['data']))
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
                correlations = df[numeric_cols].corr().to_dict()
                conversation_messages.append({
                    "name": tool_name,
                    "content": json.dumps(correlations)
                })
            
            elif tool_name == 'create_line_chart':
                df = pd.DataFrame(json.loads(tool_arguments['data']))
                chart_data = {
                    "line_chart": {
                        "x": df[tool_arguments['x']].tolist(),
                        "y": df[tool_arguments['y']].tolist(),
                        "type": "line"
                    }
                }
                conversation_messages.append({
                    "name": tool_name,
                    "content": json.dumps(chart_data)
                })
            
        except Exception as e:
            print(f"Error executing tool {tool_call.function.name}: {str(e)}")
            continue

    return conversation_messages

def handle_user_message(user_query, triaging_agent, conversation_messages=[]):
    user_message = {"role": "user", "content": user_query}
    conversation_messages.append(user_message)

    response = triaging_agent.handle_query(user_query, conversation_messages)
    
    # Handle the case where there's no tool calls
    if not hasattr(response.choices[0].message, 'tool_calls') or not response.choices[0].message.tool_calls:
        print("No tool calls found in response")
        return conversation_messages

    # Add tool calls to conversation history
    conversation_messages.extend(
        {"role": "assistant", "content": tool_call.function.name + ": " + tool_call.function.arguments}
        for tool_call in response.choices[0].message.tool_calls
    )

    # Process tool calls
    for tool_call in response.choices[0].message.tool_calls:
        if tool_call.function.name == 'send_query_to_agents':
            args = json.loads(tool_call.function.arguments)
            agents = args['agents']
            query = args['query']
            
            for agent in agents:
                try:
                    if agent == "Data Processing Agent":
                        processing_agent = ProcessingAgent(OPENAI_MODEL)
                        response = processing_agent.handle_query(query)
                        if hasattr(response.choices[0].message, 'tool_calls'):
                            execute_tool(response.choices[0].message.tool_calls, conversation_messages)
                    elif agent == "Analysis Agent":
                        analysis_agent = AnalysisAgent(OPENAI_MODEL)
                        response = analysis_agent.handle_query(query)
                        if hasattr(response.choices[0].message, 'tool_calls'):
                            execute_tool(response.choices[0].message.tool_calls, conversation_messages)
                    elif agent == "Visualization Agent":
                        visualization_agent = VisualizationAgent(OPENAI_MODEL)
                        response = visualization_agent.handle_query(query)
                        if hasattr(response.choices[0].message, 'tool_calls'):
                            execute_tool(response.choices[0].message.tool_calls, conversation_messages)
                except Exception as e:
                    print(f"Error processing {agent}: {str(e)}")
                    continue

    return conversation_messages

