from typing import Literal, cast

from langgraph.types import Command
from pydantic import BaseModel, Field

from agent.configurations import Configuration
from agent.state import State
from agent.utils import load_chat_model


class RouterResponse(BaseModel):
    """Format for router output."""

    route: Literal["chat", "finance"] = Field(
        description="Return `finance` if user request requires any financial data, otherwise return `chat`"
    )


async def router(state: State) -> Command[Literal["chat", "finance"]]:
    """Process input and returns output.

    Can use runtime configuration to alter behavior.
    """

    configuration = Configuration.from_context()
    model = load_chat_model(configuration.model).with_structured_output(RouterResponse)

    response = cast(
        RouterResponse,
        await model.ainvoke(
            [{"role": "system", "content": "You are helpfull AI CFO"}, *state["messages"]]
        ),
    )

    return Command(update={}, goto=response.route)
