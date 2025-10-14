
from workflowmanager import WorkflowManager
# for deployment on langgraph cloud
#graph = WorkflowManager().returnGraph()

manager = WorkflowManager()
manager.run_sql_agent(question="What is the relationship between market share and PD-L1 market share by laboratory?")