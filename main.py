# This is the main entry point for the multi-agent data analysis system.
# It initializes the Triaging Agent, takes a user query, and starts the conversation handling process.
# The script then prints the conversation history, providing a trace of the interactions between agents. 


from agents.triaging_agent import TriagingAgent
from utils.execution import handle_user_message
import os
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()  # Load environment variables from .env file

OPENAI_MODEL = os.getenv("OPENAI_MODEL")

def main():
    user_query = """
    I have the following sales data. Please help me:
    1. Clean the data by removing duplicates and handling any missing values
    2. Perform statistical analysis to understand the sales trends
    3. Create a line chart showing the relationship between units sold and revenue
    4. Calculate the correlation between all variables

    date, units_sold, revenue($), customer_satisfaction
    2024-01-01, 100, 5000, 4.5
    2024-01-02, 150, 7500, 4.8
    2024-01-03, 120, 6000, 4.6
    2024-01-01, 100, 5000, 4.5
    2024-01-04, 200, 10000, 4.9
    2024-01-05, 180, 9000, 4.7
    2024-01-06, null, 8500, 4.8
    """

    triaging_agent = TriagingAgent(OPENAI_MODEL)
    conversation_history = handle_user_message(user_query, triaging_agent)

    print("\n=== Analysis Results ===\n")
    for message in conversation_history:
        if message.get('name') == 'clean_data':
            print("Cleaned Data:")
            try:
                cleaned_data = json.loads(message['content'])
                df = pd.DataFrame(cleaned_data['cleaned_data'])
                print(df.to_string(index=False))
                print("\n")
            except Exception as e:
                print(f"Error displaying cleaned data: {str(e)}")
                print("Raw content:", message['content'])
                print("\n")
                
        elif message.get('name') == 'stat_analysis':
            print("Statistical Analysis:")
            try:
                stats = json.loads(json.loads(message['content'])['stats'])
                for var_name, var_stats in stats.items():
                    print(f"\n{var_name} Statistics:")
                    print(pd.DataFrame([var_stats]).to_string(index=False))
                print("\n")
            except Exception as e:
                print(f"Error displaying statistics: {str(e)}")
                print("\n")
                
        elif message.get('name') == 'correlation_analysis':
            print("Correlation Analysis:")
            try:
                correlations = json.loads(message['content'])
                print(pd.DataFrame(correlations).round(3).to_string())
                print("\n")
            except Exception as e:
                print(f"Error displaying correlations: {str(e)}")
                print("\n")
                
        elif message.get('name') == 'create_line_chart':
            try:
                result = json.loads(message['content'])
                if 'error' in result:
                    print(f"Error creating chart: {result['error']}")
                else:
                    print("Line Chart Data:")
                    print(f"X values: {result['line_chart']['x']}")
                    print(f"Y values: {result['line_chart']['y']}")
                print("\n")
            except Exception as e:
                print(f"Error displaying chart: {str(e)}")
                print("\n")

if __name__ == "__main__":
    main()

