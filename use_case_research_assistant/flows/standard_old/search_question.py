from typing import List
from promptflow.core import tool


@tool
def search_question(question: str) -> List[str]:
    # TODO: Implement the search logic
    return "helLo this is an example answer for the question: " + question

