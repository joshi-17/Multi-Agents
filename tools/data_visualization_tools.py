import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np

visualization_tools = [
    {
        "type": "function",
        "function": {
            "name": "create_bar_chart",
            "description": "Creates a bar chart from the provided data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data for the bar chart. Should be in a suitable format such as JSON or CSV."
                    },
                    "x": {
                        "type": "string",
                        "description": "Column for the x-axis."
                    },
                    "y": {
                        "type": "string",
                        "description": "Column for the y-axis."
                    }
                },
                "required": ["data", "x", "y"],
                "additionalProperties": False
            }
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "create_line_chart",
            "description": "Creates a line chart from the provided data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data for the line chart. Should be in a suitable format such as JSON or CSV."
                    },
                    "x": {
                        "type": "string",
                        "description": "Column for the x-axis."
                    },
                    "y": {
                        "type": "string",
                        "description": "Column for the y-axis."
                    }
                },
                "required": ["data", "x", "y"],
                "additionalProperties": False
            }
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "create_pie_chart",
            "description": "Creates a pie chart from the provided data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The data for the pie chart. Should be in a suitable format such as JSON or CSV."
                    },
                    "labels": {
                        "type": "string",
                        "description": "Column for the labels."
                    },
                    "values": {
                        "type": "string",
                        "description": "Column for the values."
                    }
                },
                "required": ["data", "labels", "values"],
                "additionalProperties": False
            }
        },
        "strict": True
    }
]

def create_bar_chart(data, x, y):
    # Implement your bar chart creation logic here
    bar_chart = {"bar_chart": "sample_bar_chart"}
    return bar_chart

def create_line_chart(data, x, y):
    try:
        # Convert string data to DataFrame
        data_io = StringIO(data)
        df = pd.read_csv(data_io)
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(df.iloc[:, 0], df.iloc[:, 1], 'o-', label='Data Points')
        
        # Add best fit line
        z = np.polyfit(df.iloc[:, 0], df.iloc[:, 1], 1)
        p = np.poly1d(z)
        plt.plot(df.iloc[:, 0], p(df.iloc[:, 0]), "r--", label='Trend Line')
        
        # Customize the plot
        plt.title('House Price vs Size')
        plt.xlabel('House Size (m³)')
        plt.ylabel('House Price ($)')
        plt.grid(True)
        plt.legend()
        
        # Save the plot
        plt.savefig('line_chart.png')
        plt.close()
        
        return {"line_chart": "Chart saved as line_chart.png"}
    except Exception as e:
        return {"error": str(e)}

def create_pie_chart(data, labels, values):
    # Implement your pie chart creation logic here
    pie_chart = {"pie_chart": "sample_pie_chart"}
    return pie_chart

# This file contains tools for creating different types of data visualizations, including bar charts, line charts, and pie charts.
# The `create_bar_chart`, `create_line_chart`, and `create_pie_chart` functions generate these visualizations using matplotlib.
# These tools are used by the Visualization Agent to produce visual representations of data. 