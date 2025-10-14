import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
from workflowmanager import WorkflowManager
import re
import json
# for deployment on langgraph cloud
#graph = WorkflowManager().returnGraph()

# Set up the Streamlit app
st.title("SQL Query Agent Dashboard")

# Text input for the user question
user_question = st.text_input("Enter your question:", "")

# Button to submit the question
if st.button("Submit"):
    if user_question.strip():
        # Build the workflow and process the question
        manager = WorkflowManager()
        result = manager.run_sql_agent(question=user_question)
        print("Workflow result:", result)
        # First check if we redirected them to ISC assistance
        # TODO move the expert redirect keyword to another state attribute to simplify this line 
        if result["answer"] == "This is a complicated question, please reach out to your ISC for assistance.": 
            st.subheader("Result:")
            st.write("This is a complicated question. We have altered your ISC who will be in touch to help provide these insights")
        # Check if the result contains a Plotly figure
        if isinstance(result['go_figure'], str):  # Assuming the result is a Plotly figure
            plot_json = result.get("go_figure")
            #clean json since using the agent turned it to a string 
            plot_json_clean = re.sub(r"^```json\s*|\s*```$", "", plot_json)
            plot_json_clean = json.loads(plot_json_clean)
            plot_json_clean["layout"]["template"] = "plotly_white"
            st.subheader("Generated Plot:")
            st.plotly_chart(go.Figure(plot_json_clean))  # Render the Plotly chart in Streamlit
        else:
            # Display the result if it's not a plot
            st.subheader("Result:")
            st.write(result)
    else:
        st.warning("Please enter a question before submitting.")