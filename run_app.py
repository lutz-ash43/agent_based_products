import streamlit as st
from langgraph.graph import StateGraph
from workflow import llm, toolkit, plot_tools, db, build_workflow, query_tools
from typing import TypedDict, Optional
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from utils import read_db
import os
import plotly.graph_objects as go
import plotly.io as pio

app = build_workflow(llm, query_tools, plot_tools)

# Set up the Streamlit app
st.title("SQL Query Agent Dashboard")

# Text input for the user question
user_question = st.text_input("Enter your question:", "")

# Button to submit the question
if st.button("Submit"):
    if user_question.strip():
        # Build the workflow and process the question
        app = build_workflow(llm, query_tools, plot_tools)
        result = app.invoke({"question": user_question})
        print("Workflow result:", result)
        # Check if the result contains a Plotly figure
        if isinstance(result['plot_figure'], go.Figure):  # Assuming the result is a Plotly figure
            plot_json = result.get("plot_figure")
            st.subheader("Generated Plot:")
            st.plotly_chart(plot_json)  # Render the Plotly chart in Streamlit
        else:
            # Display the result if it's not a plot
            st.subheader("Result:")
            st.write(result)
    else:
        st.warning("Please enter a question before submitting.")