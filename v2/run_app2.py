import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio
from workflowmanager import WorkflowManager
import re
import json
from run_app_utils import json_to_figure
from productInstruction import product_instructions
# for deployment on langgraph cloud
#graph = WorkflowManager().returnGraph()

# Set up the Streamlit app
st.set_page_config(layout="wide")
st.title("Agentic Lab Segmentation Application MVP")

# TODO establish 1 agent that takes in the data product as an argument is primed with descriptions of products and common insights (maybe project specific)
# generates 2 questions and returns them
# then using this input to enter the sql agent workflow twice.  Will need to save figs so make sure we can show them all

# ---- CONTAINERS ----
top_container = st.container()
bottom_container = st.container()
manager = WorkflowManager()

# ---- define product type ----
# TODO make this an argument to app not hardcoded 
prod = "labSegmentation"
prodInstructions = product_instructions[prod]

# ---- Initialize session state ----
def initialize_iia_results():
    question_list = []
    if "iia_result_1" not in st.session_state:
        st.session_state.iia_result_1 = manager.run_iia_agent(question_list, prodInstructions)
        question_list.append(st.session_state.iia_result_1["prompt_question"])
    if "iia_result_2" not in st.session_state:
        st.session_state.iia_result_2 = manager.run_iia_agent(question_list, prodInstructions)

initialize_iia_results()


# ---- TOP SECTION (Static unless page reloads) ----
with top_container:
    col1, col2 = st.columns(2)

    with col1:
        initial_q = st.session_state.iia_result_1#manager.run_iia_agent()
        st.write(initial_q["prompt_question"])
        iq_json = initial_q.get("go_figure")
        iq_fig = json_to_figure(iq_json)
        #st.subheader(initial_q["answer"])
        st.plotly_chart(go.Figure(iq_fig))
        #st.write(initial_q['prompt_question'])
        st.write(initial_q["answer"])

    with col2:
        initial_q2 = st.session_state.iia_result_2
        st.write(initial_q2["prompt_question"])
        iq_json = initial_q2.get("go_figure")
        iq_fig = json_to_figure(iq_json)
        #st.subheader(initial_q2["answer"])
        st.plotly_chart(go.Figure(iq_fig))
        #st.write(initial_q['prompt_question'])
        st.write(initial_q2["answer"])


    # Text input for the user question
    user_question = st.text_input("Enter your question:", "")
    submit_button = st.button("Submit")
# Button to submit the question
if submit_button: #st.button("Submit"):
    with bottom_container: 
        if user_question.strip():
            # Build the workflow and process the question
            #manager = WorkflowManager()
            result = manager.run_sql_agent(question=user_question, product=prodInstructions)
            print("Workflow result:", result)
            # First check if we redirected them to ISC assistance
            # TODO move the expert redirect keyword to another state attribute to simplify this line 
            # TODO move this parsing function a utility file and save as a fig
            if result["answer"] == "This is a complicated question, please reach out to your ISC for assistance.": 
                st.subheader("Result:")
                st.write("This is a complicated question. We have altered your ISC who will be in touch to help provide these insights")
            # Check if the result contains a Plotly figure
            if isinstance(result['go_figure'], str):  # Assuming the result is a Plotly figure
                plot_json = result.get("go_figure")
                #clean json since using the agent turned it to a string 
                # plot_json_clean = re.sub(r"^```json\s*|\s*```$", "", plot_json)
                # plot_json_clean = json.loads(plot_json_clean)
                # plot_json_clean["layout"]["template"] = "plotly_white"
                go_fig = json_to_figure(plot_json)
                st.subheader("Generated Plot:")
                st.plotly_chart(go.Figure(go_fig))  # Render the Plotly chart in Streamlit
                # adding one line human readable summary 
                st.subheader("Summary:")
                st.write(result["answer"])
            else:
                # Display the result if it's not a plot
                st.subheader("Result:")
                st.write(result)
        else:
            st.warning("Please enter a question before submitting.")