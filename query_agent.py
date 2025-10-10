from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from typing import List, Dict, Any, Optional

# @tool
# def create_bar_chart(
#     data: List[Dict[str, Any]], x_col: str, y_col: str, title: str, color_col: Optional[str] = None
# ):
#     """Creates a bar chart from a list of dicts using plotly.express."""
#     import plotly.express as px
#     df = pd.DataFrame(data)
#     fig = px.bar(df, x=x_col, y=y_col, color=color_col if color_col else None, title=title)
#     #fig.show()
#     return {"fig": fig.to_json(), "title": title}

def create_query_agent(llm, tools):
    # import SQL database toolkit
    #toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    #tools = toolkit.get_tools()

    system_message = """
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run,
    then look at the results of the query and return the answer. Unless the user
    specifies a specific number of examples they wish to obtain, always limit your
    query to at most {top_k} results.

    You can order the results by a relevant column to return the most interesting
    examples in the database. Never query for all the columns from a specific table,
    only ask for the relevant columns given the question.

    You MUST alias columns using the `AS` keyword to ensure the output has readable column names. For example, use `lab_type AS LabType`, `test_type AS TestType`, and `AVG(turnaround_time) AS AvgTAT`.

    You MUST double check your query before executing it. If you get an error while
    executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the
    database.

    To start you should ALWAYS look at the tables in the database to see what you
    can query. Do NOT skip this step.

    the labseg table contains data where each row is a unique assay laboratory combination. 
    Data such as market share, turn around time, and other columns some of which are prefixed by LAB LEVEL are the same for all instances of the same lab. 
    Other columns pertain to the individual assays each lab offers. Be sure to check that data is not duplicated at the lab level when returning certain results.

    Then you should query the schema of the most relevant tables.
    """.format(
        dialect="SQLite",
        top_k=100,
    )
    # TO DO add the table context and some few shots examples as well as a description of the table
    return(create_react_agent(llm, tools, prompt=system_message))
