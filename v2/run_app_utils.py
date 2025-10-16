import json
import plotly.graph_objects as go
import re

def json_to_figure(plot_json):
    plot_json_clean = re.sub(r"^```json\s*|\s*```$", "", plot_json)
    plot_json_clean = json.loads(plot_json_clean)
    plot_json_clean["layout"]["template"] = "plotly_white"
    return(go.Figure(plot_json_clean))