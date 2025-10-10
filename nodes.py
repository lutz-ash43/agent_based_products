import ast
from query_agent import create_query_agent
from plot_agent import create_plot_agent
from utils import convert_sql_result_to_dict
import json
import plotly.io as pio
from utils import figure_dict_to_json

# def make_query_node(llm, tools):
#     agent = create_query_agent(llm, tools)
#     def node(state):
#         question = state["question"]
#         sql_result = None
#         for step in agent.stream(
#             {"messages": [{"role": "user", "content": question}]},
#             stream_mode="values",
#         ):
#             for msg in step["messages"]:
#                 if hasattr(msg, "name") and msg.name == "sql_db_query":
#                     sql_result = msg.content if hasattr(msg, "content") else getattr(msg, "tool_output", None)
#                 # TODO check to see if we can propogate the query to get the column names 
#                 if hasattr(msg, "arguments"):
#                     args = msg.arguments
#                     if isinstance(args, str):
#                         args = json.loads(args)
#                         sql_query = args.get("query") or args.get("sql")
#                         print("QUERY")
#                         print(sql_query)

#         return {**state, "sql_result": sql_result}
#     return node

# TODO this our better query agent call bc it removes the loop 
def make_query_node(llm, tools):
    agent = create_query_agent(llm, tools)

    def node(state):
        question = state["question"]

        # Run the agent synchronously
        result = agent.invoke({"messages": [{"role": "user", "content": question}]})

        # Extract the sql_db_query result if present
        sql_msg = next(
            (
                msg for msg in result.get("messages", [])
                if getattr(msg, "name", None) == "sql_db_query"
            ),
            None
        )

        sql_result = getattr(sql_msg, "content", getattr(sql_msg, "tool_output", None)) if sql_msg else None

        return {**state, "sql_result": sql_result}

    return node

def make_plot_node(llm, tools):
    agent = create_plot_agent(llm, tools)
    def node(state):
        sql_result = state.get("sql_result")
        question = state.get("question")
        # print("QUESTION")
        # print(question)
        # query_string = state.get("query")
        # print("QUERY STRING")
        # print(query_string)
        if sql_result:
            dict_list = convert_sql_result_to_dict(sql_result)
        else:
            print("No SQL result to plot.")
            return state
       
        plot_instruction = f"Plot {question}."
        plot_figure = None
        plot_title = None
        for step in agent.stream(
            {"messages": [
                {"role": "user", "content": plot_instruction},
                {"role": "system", "content": f"Here is the data: {dict_list}"}
            ]},
            stream_mode="values",
        ):
            for msg in step["messages"]:
                # Check if it's a ToolMessage from a plotting tool
                if hasattr(msg, "name") and isinstance(msg.name, str) and "create_" in msg.name:
                    try:
                        tool_output = msg.content
                        print("ToolMessage content:", tool_output)
                        print("Type of tool output:", type(tool_output))

                        # If tool_output is a string, parse it as JSON
                        if isinstance(tool_output, str):
                            tool_output_dict = json.loads(tool_output)  # Convert string to dict
                            fig_json_str = tool_output_dict.get("fig")

                            if fig_json_str:
                                plot_figure = pio.from_json(fig_json_str)
                                print("Successfully parsed Plotly figure:", type(plot_figure))
                                #plot_figure.show()  # Or save/display as needed
                            else:
                                print("No 'fig' key found in tool output.")
                        else:
                            print("Tool output is not a string.")
                    except Exception as e:
                        print("Failed to parse Plotly figure:", e)
                print("PLOT FIGURE:", plot_figure)
        if plot_figure:
            return {**state, "plot_data": str(dict_list), "plot_figure": plot_figure, "plot_title": plot_title}

        else:
            print("No plot generated.")
            return state
    return node
