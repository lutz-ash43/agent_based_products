import ast
import sqlite3
from langchain_community.utilities import SQLDatabase
import plotly.io as pio

def convert_sql_result_to_dict(sql_result):
    tuple_list = ast.literal_eval(sql_result)
    print(tuple_list)
    # Dynamically infer keys based on length of tuples
    keys = ["column_" + str(i) for i in range(len(tuple_list[0]))]
    dict_list = [dict(zip(keys, row)) for row in tuple_list]
    return dict_list

def read_db(db_path):
    conn = sqlite3.connect("lab_seg.db")
    #data2.to_sql("labseg", conn, if_exists="replace", index=False)

    # Create SQLDatabase object from the new SQLite DB
    db = SQLDatabase.from_uri("sqlite:///lab_seg.db")
    print(db.dialect)
    print(db.get_usable_table_names())
    return(db)

def figure_dict_to_json(fig_dict):
    # If input is a dict with 'fig' key, extract the Figure object
    fig = fig_dict.get('fig', None)
    if fig is not None and hasattr(fig, 'to_dict'):
        # Convert Figure to dict, then to JSON
        fig_json = pio.to_json(fig)
        return fig_json
    else:
        raise ValueError("Input must be a dict with a Plotly Figure under the 'fig' key.")