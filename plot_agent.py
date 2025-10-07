from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from typing import List, Dict, Any
import pandas as pd
import plotly_express as px

from langchain.chat_models import init_chat_model

#llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

@tool
def create_bar_chart(
    data: List[Dict[str, Any]], x_col: str, y_col: str, title: str
):
    """Creates a bar chart from a list of dicts using plotly.express."""
    import plotly.express as px
    df = pd.DataFrame(data)
    fig = px.bar(df, x=x_col, y=y_col, title=title)
    #fig.show()
    return {"fig": fig.to_json(), "title": title}

@tool
def create_line_chart(
    data: List[Dict[str, Any]], x_col: str, y_col: str, title: str
):
    """Creates a line chart from a list of dicts using plotly.express."""
    import plotly.express as px
    df = pd.DataFrame(data)
    fig = px.line(df, x=x_col, y=y_col, title=title)
    #fig.show()
    return {"fig": fig.to_json(), "title": title}

@tool
def create_scatter_plot(
    data: List[Dict[str, Any]], x_col: str, y_col: str, title: str
):
    """Creates a scatter plot from a list of dicts using plotly.express."""
    import plotly.express as px
    df = pd.DataFrame(data)
    fig = px.scatter(df, x=x_col, y=y_col, title=title)
    #fig.show()
    return {"fig": fig.to_json(), "title": title}

def collect_plot_tools():
    return [create_bar_chart, create_line_chart, create_scatter_plot]

def create_plot_agent(llm, tools):
    #plot_tools = [create_bar_chart, create_line_chart, create_scatter_plot]

    plot_description_prompt = """
    You are a visualization agent. Given tabular data and a user instruction, select the most appropriate plot type (bar, line, scatter) and plot it using the available tools.
    Reason step by step about the data and the user's intent before choosing a plot.
    """

    return(create_react_agent(llm, tools, prompt=plot_description_prompt))