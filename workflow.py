from langgraph.graph import StateGraph
from plot_agent import collect_plot_tools
from nodes import make_query_node, make_plot_node
from typing import TypedDict, Optional
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from utils import read_db
import os

# Define llm db and tools 
if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = 'AIzaSyCBV903MIqJH6pMAxuY0iCC4xjF5Pn1TZw'

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

db = read_db("../lab_seg.db")

plot_tools = collect_plot_tools()
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
query_tools = toolkit.get_tools()

class AgentState(TypedDict):
    question: str
    sql_result: Optional[str]
    plot_data: Optional[str]
    plot_figure: Optional[object]

def build_workflow(llm, query_tools, plot_tools):
    graph = StateGraph(AgentState)

    graph.add_node("query_agent", make_query_node(llm, query_tools))
    graph.add_node("plot_agent", make_plot_node(llm, plot_tools))

    graph.set_entry_point("query_agent")
    graph.add_edge("query_agent", "plot_agent")

    return graph.compile()

# run
app = build_workflow(llm, query_tools, plot_tools)
#result = app.invoke({"question": "Show market share by laboratory"})
