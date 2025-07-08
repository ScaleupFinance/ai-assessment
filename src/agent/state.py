from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import MessagesState, add_messages


class InputState(MessagesState):
    """Input State"""


class State(InputState):
    """Full State"""

    finance_messages: Annotated[list[AnyMessage], add_messages]
