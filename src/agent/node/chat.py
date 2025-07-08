"""Chat agent"""

from typing import Literal, cast

from langchain_core.messages import AIMessage
from langgraph.types import Command

from agent.configurations import Configuration
from agent.state import State
from agent.utils import load_chat_model


async def chat(state: State) -> Command[Literal["__end__"]]:
    configuration = Configuration.from_context()
    model = load_chat_model(configuration.model)

    response = cast(
        AIMessage,
        await model.ainvoke(
            [{"role": "system", "content": "You are helpfull AI CFO"}, *state["messages"]]
        ),
    )

    return Command(update={"messages": [response]}, goto="__end__")
