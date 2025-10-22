import json
from langchain_core.prompts import ChatPromptTemplate
from llm_manager import LLMManager
from graph_instructions import graph_instructions
import json


class DataFormatter:
    def __init__(self):
        self.llm_manager = LLMManager()

    
    def format_data_for_visualization(self, state: dict) -> dict:
        """Format the data for the chosen visualization type."""
        visualization = state['visualization']
        results = state['results']
        question = state['question']
        sql_query = state['sql_query']

        if visualization == "none":
            return {"formatted_data_for_visualization": None}
        
        if visualization == "scatter":
            print("viz_detected")
            try:
                return self._format_scatter_data(results)
            except Exception as e:
                return self._format_other_visualizations(visualization, question, sql_query, results)
        
        if visualization == "bar" or visualization == "horizontal_bar":
            print("viz detected")
            try:
                return self._format_bar_data(results, question)
            except Exception as e:
                return self._format_other_visualizations(visualization, question, sql_query, results)
        
        if visualization == "line":
            try:
                return self._format_line_data(results, question)
            except Exception as e:
                return self._format_other_visualizations(visualization, question, sql_query, results)
        
        if visualization == "box":
            try:
                print("Box Selected")
                return self._format_box_data(results)
            except Exception as e:
                return self._format_other_visualizations(visualization, question, sql_query, results)
        
        return self._format_other_visualizations(visualization, question, sql_query, results)
    
    def format_data_for_visualization_iia(self, state: dict) -> dict:
        """Format the data for the chosen visualization type."""
        visualization = state['visualization']
        results = state['results']
        question = state['prompt_question']
        sql_query = state['sql_query']

        if visualization == "none":
            return {"formatted_data_for_visualization": None}
        
        if visualization == "scatter":
            print("viz_detected")
            try:
                return self._format_scatter_data(results)
            except Exception as e:
                return self._format_other_visualizations(visualization, question, sql_query, results)
        
        if visualization == "bar" or visualization == "horizontal_bar":
            print("viz detected")
            try:
                return self._format_bar_data(results, question)
            except Exception as e:
                return self._format_other_visualizations(visualization, question, sql_query, results)
        
        if visualization == "line":
            try:
                return self._format_line_data(results, question)
            except Exception as e:
                return self._format_other_visualizations(visualization, question, sql_query, results)

        if visualization == "box":
            try:
                return self._format_box_data(results)
            except Exception as e:
                return self._format_other_visualizations(visualization, question, sql_query, results)
        
        return self._format_other_visualizations(visualization, question, sql_query, results)
    
    def _format_line_data(self, results, question):
        if isinstance(results, str):
            results = eval(results)

        if len(results[0]) == 2:

            x_values = [str(row[0]) for row in results]
            y_values = [float(row[1]) for row in results]

            # Use LLM to get a relevant label
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a data labeling expert. Given a question and some data, provide a concise and relevant label for the data series."),
                ("human", "Question: {question}\n Data (first few rows): {data}\n\nProvide a concise label for this y axis. For example, if the data is the sales figures over time, the label could be 'Sales'. If the data is the population growth, the label could be 'Population'. If the data is the revenue trend, the label could be 'Revenue'."),
            ])
            label = self.llm_manager.invoke(prompt, question=question, data=str(results[:2]))

            formatted_data = {
                "xValues": x_values,
                "yValues": [
                    {
                        "data": y_values,
                        "label": label.strip()
                    }
                ]
            }
        elif len(results[0]) == 3:

            # Group data by label
            data_by_label = {}
            x_values = []

            # Get a list of unique labels
            labels = list(set(item2 for item1, item2, item3 in results 
                              if isinstance(item2, str) and not item2.replace(".", "").isdigit() and "/" not in item2))
            
            # If labels are not in the second position, check the first position
            if not labels:
                labels = list(set(item1 for item1, item2, item3 in results 
                                  if isinstance(item1, str) and not item1.replace(".", "").isdigit() and "/" not in item1))

            for item1, item2, item3 in results:
                # Determine which item is the label (string not convertible to float and not containing "/")
                if isinstance(item1, str) and not item1.replace(".", "").isdigit() and "/" not in item1:
                    label, x, y = item1, item2, item3
                else:
                    x, label, y = item1, item2, item3
                    

                if str(x) not in x_values:
                    x_values.append(str(x))
                if label not in data_by_label:
                    data_by_label[label] = []
                data_by_label[label].append(float(y))
                print(labels)
                for other_label in labels:
                    if other_label != label:
                        if other_label not in data_by_label:
                            data_by_label[other_label] = []
                        data_by_label[other_label].append(None)

            # Create yValues array
            y_values = [
                {
                    "data": data,
                    "label": label
                }
                for label, data in data_by_label.items()
            ]

            formatted_data = {
                "xValues": x_values,
                "yValues": y_values,
                "yAxisLabel": ""
            }

            # Use LLM to get a relevant label for the y-axis
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a data labeling expert. Given a question and some data, provide a concise and relevant label for the y-axis."),
                ("human", "Question: {question}\n Data (first few rows): {data}\n\nProvide a concise label for the y-axis. For example, if the data represents sales figures over time for different categories, the label could be 'Sales'. If it's about population growth for different groups, it could be 'Population'."),
            ])
            y_axis_label = self.llm_manager.invoke(prompt, question=question, data=str(results[:2]))

            # Add the y-axis label to the formatted data
            formatted_data["yAxisLabel"] = y_axis_label.strip()

        return {"formatted_data_for_visualization": formatted_data}

    def _format_scatter_data(self, results):
        print(results)
        if isinstance(results, str):
            print("results is string :", results)
            results = eval(results)

        formatted_data = {"series": []}
        
        if len(results[0]) == 2:
            print("results is 2d", results)
            formatted_data["series"].append({
                "data": [
                    {"x": float(x), "y": float(y), "id": i+1}
                    for i, (x, y) in enumerate(results)
                ],
                "label": "Data Points"
            })
        elif len(results[0]) == 3:
            entities = {}
            for item1, item2, item3 in results:
                # Determine which item is the label (string not convertible to float and not containing "/")
                if isinstance(item1, str) and not item1.replace(".", "").isdigit() and "/" not in item1:
                    label, x, y = item1, item2, item3
                else:
                    x, label, y = item1, item2, item3
                if label not in entities:
                    entities[label] = []
                entities[label].append({"x": float(x), "y": float(y), "id": len(entities[label])+1})
            
            for label, data in entities.items():
                formatted_data["series"].append({
                    "data": data,
                    "label": label
                })
        else:
            raise ValueError("Unexpected data format in results")                

        return {"formatted_data_for_visualization": formatted_data}

    def _format_scatter_data(self, results):
        print("Original results:", results)

        # If results is a string, evaluate it to convert to list of dicts
        if isinstance(results, str):
            print("results is string:", results)
            results = eval(results)

        formatted_data = {"series": []}

        # Check if results is a list of dictionaries
        if isinstance(results, list) and isinstance(results[0], dict):
            for i, entry in enumerate(results):
                # Extract numeric keys dynamically
                numeric_items = [(k, v) for k, v in entry.items() if isinstance(v, (int, float))]
                if len(numeric_items) == 2:
                    x_key, x_val = numeric_items[0]
                    y_key, y_val = numeric_items[1]
                    formatted_data["series"].append({
                        "data": [{"x": float(x_val), "y": float(y_val), "id": i + 1}],
                        "label": f"Point {i + 1}"
                    })
                else:
                    raise ValueError(f"Entry {i} does not contain at least two numeric values.")
        else:
            raise ValueError("Unexpected data format in results")

        return {"formatted_data_for_visualization": formatted_data}


    def _format_bar_data(self, results, question):
        if isinstance(results, str):
            results = eval(results)
            print("reusults is string :", results)
        if len(results[0]) == 2:
            print("reslts is 2d", results)
            # Simple bar chart with one series
            #labels = [str(row[0]) for row in results]
            labels = [next(iter(d.values())) for d in results]
            print('labels', labels)
            #data = [float(row[1]) for row in results]
            data = [list(d.values())[1] for d in results if len(d) > 1]
            
            # Use LLM to get a relevant label
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a data labeling expert. Given a question and some data, provide a concise and relevant label for the data series."),
                ("human", "Question: {question}\nData (first few rows): {data}\n\nProvide a concise label for this y axis. For example, if the data is the sales figures for products, the label could be 'Sales'. If the data is the population of cities, the label could be 'Population'. If the data is the revenue by region, the label could be 'Revenue'."),
            ])
            label = self.llm_manager.invoke(prompt, question=question, data=str(results[:2]))
            
            values = [{"data": data, "label": label}]
        elif len(results[0]) == 3:
            print("reslts is 3d", results)
            # Grouped bar chart with multiple series
            categories = set(row[1] for row in results)
            labels = list(categories)
            entities = set(row[0] for row in results)
            values = []
            for entity in entities:
                entity_data = [float(row[2]) for row in results if row[0] == entity]
                values.append({"data": entity_data, "label": str(entity)})
        else:
            raise ValueError("Unexpected data format in results")

        formatted_data = {
            "labels": labels,
            "values": values
        }
        print("bar chart")
        #print("formatted data:", formatted_data)
        return {"formatted_data_for_visualization": formatted_data}
    

    # attempt to allow 3 categories 
    def _format_bar_data(self, results, question):
        if isinstance(results, str):
            results = eval(results)
            print("results is string:", results)

        if len(results[0]) == 2:
            print("results is 2D:", results)

            labels = [next(iter(d.values())) for d in results]
            print("labels:", labels)

            data = [list(d.values())[1] for d in results if len(d) > 1]

            # Use LLM to label the y-axis
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a data labeling expert. Given a question and some data, provide a concise and relevant label for the data series."),
                ("human", "Question: {question}\nData (first few rows): {data}\n\nProvide a concise label for this y axis."),
            ])
            label = self.llm_manager.invoke(prompt, question=question, data=str(results[:2]))

            values = [{"data": data, "label": label}]
        
        elif isinstance(results[0], dict) and len(results[0]) == 3:
            print("results is grouped dict (3 keys):", results)

            # Infer keys
            sample = results[0]
            keys = list(sample.keys())
            color_key = keys[0]
            label_key = keys[1]
            value_key = keys[2]

            labels = sorted(list(set(row[label_key] for row in results)))
            color_groups = sorted(list(set(row[color_key] for row in results)))

            values = []
            for color_group in color_groups:
                group_data = []
                for label in labels:
                    match = next((row for row in results if row[color_key] == color_group and row[label_key] == label), None)
                    group_data.append(float(match[value_key]) if match else 0)
                
                values.append({
                    "data": group_data,
                    "label": color_group,  # Grouping category becomes the label
                    "color": color_group   # Plotly can use this for categorical color mapping
                })

        else:
            raise ValueError("Unexpected data format in results")

        formatted_data = {
            "labels": labels,
            "values": values
        }

        print("Formatted bar chart data:", formatted_data)
        return {"formatted_data_for_visualization": formatted_data}
    
    def _format_box_data(self, results):
        print("Raw results:", results)

        if isinstance(results, str):
            print("Results is a string; evaluating...")
            results = eval(results)

        formatted_data = {"labels": [], "values": []}

        for item in results:
            try:
                label = item["laboratory_type"]
                min_val = item["min_market_share"]
                q1 = item["q1_market_share"]
                median = item["median_market_share"]
                q3 = item["q3_market_share"]
                max_val = item["max_market_share"]
            except KeyError as e:
                raise ValueError(f"Missing expected key in item: {e}")

            value_entry = {
                "min": float(min_val),
                "q1": float(q1),
                "median": float(median),
                "q3": float(q3),
                "max": float(max_val),
                "label": label
            }

            formatted_data["labels"].append(label)
            formatted_data["values"].append(value_entry)

        return {"formatted_data_for_visualization": formatted_data}


    def _format_box_data(self, results):
        print("Raw results:", results)

        if isinstance(results, str):
            print("Results is a string; evaluating...")
            results = eval(results)

        formatted_data = {"labels": [], "values": []}

        for item in results:
            if not isinstance(item, dict):
                raise ValueError(f"Each item must be a dictionary: {item}")

            keys = list(item.keys())
            values = list(item.values())

            if len(values) < 6:
                raise ValueError(f"Each item must have at least 6 fields (label, min, q1, median, q3, max): {item}")

            label = keys[0]
            min_val = values[1]
            q1 = values[2]
            median = values[3]
            q3 = values[4]
            max_val = values[5]

            if not isinstance(label, str):
                raise ValueError(f"First value must be a string label: {label}")
            
            value_entry = {
                "min": float(min_val),
                "q1": float(q1),
                "median": float(median),
                "q3": float(q3),
                "max": float(max_val),
                "label": label
            }

            formatted_data["labels"].append(label)
            formatted_data["values"].append(value_entry)

        return {"formatted_data_for_visualization": formatted_data}
    

    def _format_other_visualizations(self, visualization, question, sql_query, results):
        instructions = graph_instructions[visualization]
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a Data expert who formats data according to the required needs. You are given the question asked by the user, it's sql query, the result of the query and the format you need to format it in."),
            ("human", 'For the given question: {question}\n\nSQL query: {sql_query}\n\Result: {results}\n\nUse the following example to structure the data: {instructions}. Just give the json string. Do not format it'),
        ])
        response = self.llm_manager.invoke(prompt, question=question, sql_query=sql_query, results=results, instructions=instructions)
 
        try:
            formatted_data_for_visualization = json.loads(response)
            print('other viz')
            #print(formatted_data_for_visualization)
            return {"formatted_data_for_visualization": formatted_data_for_visualization}
        except json.JSONDecodeError:
            return {"error": "Failed to format data for visualization", "raw_response": response}

    def make_plotly_go(self, state: dict) -> dict:
            visualization = state["visualization"]
            question = state["question"] 
            query= state["sql_query"]
            results = state["results"]
            formatted_data_for_visualization= state["formatted_data_for_visualization"]
            """convert visualization into a plotly go json for application"""
            prompt = ChatPromptTemplate.from_messages([
                ('''system", "You are a Data expert who turns formatted data into useful plotly.express visualizations. 
                you are given a list of formatted data for the visualization where the labels and values are defined as well as the type of graph to generate and generate axes labels and legends.
                You are also given the question the user asks, use this to inform the plot title and any other annotation such as hover_data. 
                You also have access to the resutls and sql query to further inform your visualization. 
                You MUST return input in acceptable json form for a go.Figure to be unpacked by the pio.from_json package'''),
                ("human", 'For the given question: {question}\n\nSQL query: {sql_query}\n\Result: {results}\n\nUse the following formatted data: {formatted_data_for_visualization} to generate a {visualization} as a json go.figure output'),
            ])
            response = self.llm_manager.invoke(prompt, question=question, sql_query=query, results=results, visualization=visualization, formatted_data_for_visualization=formatted_data_for_visualization)

            return {"go_figure": response}
    
    def make_plotly_go_iia(self, state: dict) -> dict:
            visualization = state["visualization"]
            question = state["prompt_question"] 
            query= state["sql_query"]
            results = state["results"]
            formatted_data_for_visualization= state["formatted_data_for_visualization"]
            """convert visualization into a plotly go json for application"""
            prompt = ChatPromptTemplate.from_messages([
                ('''system", "You are a Data expert who turns formatted data into useful plotly.express visualizations. 
                you are given a list of formatted data for the visualization where the labels and values are defined as well as the type of graph to generate and generate axes labels and legends.
                You are also given the question the user asks, use this to inform the plot title and any other annotation such as hover info. 
                You also have access to the results and sql query to further inform your visualization. 
                
                Before returning ensure that all formatting is correct including the string formatting for hoverinfo. The hoverinfo should contain no special characters if different from default.
                
                You MUST return input in acceptable json form for a go.Figure to be unpacked by the pio.from_json package'''),
                ("human", 'For the given question: {question}\n\nSQL query: {sql_query}\n\Result: {results}\n\nUse the following formatted data: {formatted_data_for_visualization} to generate a {visualization} as a json go.figure output'),
            ])
            response = self.llm_manager.invoke(prompt, question=question, sql_query=query, results=results, visualization=visualization, formatted_data_for_visualization=formatted_data_for_visualization)

            return {"go_figure": response}