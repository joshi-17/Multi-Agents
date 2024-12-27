import pandas as pd
from io import StringIO
import statsmodels.api as sm

analysis_tools = [
    {
        "type": "function",
        "function": {
            "name": "stat_analysis",
            "description": "Performs statistical analysis on the given dataset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The dataset to analyze. Should be in a suitable format such as JSON or CSV."
                    }
                },
                "required": ["data"],
                "additionalProperties": False
            }
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "correlation_analysis",
            "description": "Calculates correlation coefficients between variables in the dataset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The dataset to analyze. Should be in a suitable format such as JSON or CSV."
                    },
                    "variables": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of variables to calculate correlations for."
                    }
                },
                "required": ["data", "variables"],
                "additionalProperties": False
            }
        },
        "strict": True
    },
    {
        "type": "function",
        "function": {
            "name": "regression_analysis",
            "description": "Performs regression analysis on the dataset.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "The dataset to analyze. Should be in a suitable format such as JSON or CSV."
                    },
                    "dependent_var": {
                        "type": "string",
                        "description": "The dependent variable for regression."
                    },
                    "independent_vars": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of independent variables."
                    }
                },
                "required": ["data", "dependent_var", "independent_vars"],
                "additionalProperties": False
            }
        },
        "strict": True
    }
]

def stat_analysis(data):
    data_io = StringIO(data)
    df = pd.read_csv(data_io, sep=",")
    return df.describe().to_json()

def correlation_analysis(data, variables):
    data_io = StringIO(data)
    df = pd.read_csv(data_io, sep=",")
    correlation_matrix = df[variables].corr()
    return correlation_matrix.to_json()

def regression_analysis(data, dependent_var, independent_vars):
    data_io = StringIO(data)
    df = pd.read_csv(data_io, sep=",")
    X = df[independent_vars]
    X = sm.add_constant(X)  # Adds a constant term to the predictor
    y = df[dependent_var]
    model = sm.OLS(y, X).fit()
    return model.summary().as_json()

# This file provides tools for performing statistical analysis, correlation analysis, and regression analysis on data.
# The `stat_analysis` function computes descriptive statistics, `correlation_analysis` calculates correlation coefficients, and `regression_analysis` performs linear regression.
# These tools are utilized by the Analysis Agent to conduct various data analyses.