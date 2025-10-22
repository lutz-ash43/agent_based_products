from typing import List, Any, Annotated, Dict, Optional
from typing_extensions import TypedDict
import operator

class InputState(TypedDict):
    question: str
    question_list : list[str]
    product : str
    parsed_question: Dict[str, Any]
    unique_nouns: List[str]
    sql_query: str
    results: List[Any]
    visualization: Annotated[str, operator.add]
    go_figure : Dict[str, Any]

class OutputState(TypedDict):
    #parsed_question: Dict[str, Any]
    #unique_nouns: List[str]
    sql_query: str
    product : str
    sql_valid: bool
    sql_issues: str
    results: List[Any]
    answer: Annotated[str, operator.add]
    error: str
    visualization: Annotated[str, operator.add]
    visualization_reason: Annotated[str, operator.add]
    formatted_data_for_visualization: Dict[str, Any]
    go_figure : Dict[str, Any]
    prompt_question : str


class WorkflowState(InputState, OutputState):
    pass
