from langgraph.graph import StateGraph
from state import InputState, OutputState, WorkflowState
from sqlagent import SQLAgent
from initial_insights_agent import InitialInsightsAgent
from dataformatter import DataFormatter
from langgraph.graph import END

class WorkflowManager:
    def __init__(self):
        self.sql_agent = SQLAgent()
        self.iia_agent = InitialInsightsAgent()
        self.data_formatter = DataFormatter()

    def create_workflow(self) -> StateGraph:
        """Create and configure the workflow graph."""
        workflow = StateGraph(state_schema=WorkflowState, input=InputState, output=OutputState)

        # Add nodes to the graph
        #workflow.add_node("parse_question", self.sql_agent.parse_question)
        #workflow.add_node("get_unique_nouns", self.sql_agent.get_unique_nouns)
        workflow.add_node("generate_sql", self.sql_agent.generate_sql)
        workflow.add_node("validate_and_fix_sql", self.sql_agent.validate_and_fix_sql)
        workflow.add_node("execute_sql", self.sql_agent.execute_sql)
        workflow.add_node("format_results", self.sql_agent.format_results)
        workflow.add_node("choose_visualization", self.sql_agent.choose_visualization)
        workflow.add_node("format_data_for_visualization", self.data_formatter.format_data_for_visualization)
        workflow.add_node("make_plotly_go", self.data_formatter.make_plotly_go)
        
        # Define edges
        #workflow.add_edge("parse_question", "get_unique_nouns")
        #workflow.add_edge("get_unique_nouns", "generate_sql")
        workflow.add_edge("generate_sql", "validate_and_fix_sql")
        workflow.add_edge("validate_and_fix_sql", "execute_sql")
        workflow.add_edge("execute_sql", "format_results")
        workflow.add_edge("execute_sql", "choose_visualization")
        workflow.add_edge("choose_visualization", "format_data_for_visualization")
        workflow.add_edge("format_data_for_visualization", "make_plotly_go")
        workflow.add_edge("make_plotly_go", END)
        workflow.add_edge("format_results", END)
        workflow.set_entry_point("generate_sql")

        return workflow

    def create_workflow_iia(self) -> StateGraph:
        """Create and configure the workflow graph."""
        workflow = StateGraph(state_schema=WorkflowState, input=InputState, output=OutputState)

        # Add nodes to the graph
        # TODO comment out all but the first node since we know the rest works 
        
        #workflow.add_node("parse_question", self.sql_agent.parse_question)
        #workflow.add_node("get_unique_nouns", self.sql_agent.get_unique_nouns)
        workflow.add_node("generate_insights", self.iia_agent.generate_initial_prompts)
        workflow.add_node("generate_sql_iia", self.iia_agent.generate_sql_iia)
        workflow.add_node("validate_and_fix_sql_iia", self.iia_agent.validate_and_fix_sql_iia)
        workflow.add_node("execute_sql_iia", self.iia_agent.execute_sql_iia)
        workflow.add_node("format_results_iia", self.iia_agent.format_results_iia)
        workflow.add_node("choose_visualization_iia", self.iia_agent.choose_visualization_iia)
        workflow.add_node("format_data_for_visualization_iia", self.data_formatter.format_data_for_visualization_iia)
        workflow.add_node("make_plotly_go_iia", self.data_formatter.make_plotly_go_iia)
        
        # Define edges
        #workflow.add_edge("parse_question", "get_unique_nouns")
        workflow.add_edge("generate_insights", "generate_sql_iia")
        workflow.add_edge("generate_sql_iia", "validate_and_fix_sql_iia")
        workflow.add_edge("validate_and_fix_sql_iia", "execute_sql_iia")
        workflow.add_edge("execute_sql_iia", "format_results_iia")
        workflow.add_edge("format_results_iia", "choose_visualization_iia")
        workflow.add_edge("choose_visualization_iia", "format_data_for_visualization_iia")
        workflow.add_edge("format_data_for_visualization_iia", "make_plotly_go_iia")
        workflow.add_edge("make_plotly_go_iia", END)
        workflow.add_edge("format_results_iia", END)
        workflow.set_entry_point("generate_insights")

        return workflow
    
    def returnGraph(self):
        return self.create_workflow().compile()

    def run_sql_agent(self, question: str) -> dict:
        """Run the SQL agent workflow and return the formatted answer and visualization recommendation."""
        app = self.create_workflow().compile()
        result = app.invoke({"question": question})
        return {
            "answer": result['answer'],
            "visualization": result['visualization'],
            "visualization_reason": result['visualization_reason'],
            "formatted_data_for_visualization": result['formatted_data_for_visualization'],
            "go_figure": result["go_figure"]
        }
    def run_iia_agent(self):
        app = self.create_workflow_iia().compile()
        result = app.invoke({}) #we need to adjust the output here probably how the iia class is parsing output to establish our json organization
        print(result)
        return {
            "prompt_question": result['prompt_question'],
            "answer" : result["answer"],
            "visualization": result['visualization'],
            "visualization_reason": result['visualization_reason'],
            "formatted_data_for_visualization": result['formatted_data_for_visualization'],
            "go_figure": result["go_figure"]
        }