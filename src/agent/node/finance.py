"""Chat agent"""

from typing import Literal, cast

from langchain_core.messages import AIMessage
from langgraph.types import Command

from agent.configurations import Configuration
from agent.state import State
from agent.tools import financial_statements_tool, retriever_tool
from agent.utils import get_next_tool, load_chat_model


async def finance(
    state: State,
) -> Command[Literal["financial_statements_tool", "retriever_tool", "__end__"]]:
    configuration = Configuration.from_context()
    model = load_chat_model(configuration.model).bind_tools(
        [financial_statements_tool, retriever_tool]
    )

    response = cast(
        AIMessage,
        await model.ainvoke(
            [
                {"role": "system", "content": "You are helpfull AI CFO"},
                state["messages"][-1],
                *state["finance_messages"],
            ]
        ),
    )

    tool = get_next_tool(getattr(response, "tool_calls", None))

    # Map tool names to graph node names
    tool_node_mapping = {
        "financial_statements_tool": "financial_statements_tool",
        "retrieve_report_data": "retriever_tool",
    }

    # Get the actual node name from the mapping
    node_name = tool_node_mapping.get(tool, tool) if tool else "__end__"

    return Command(
        update={"messages": [] if tool else [response], "finance_messages": [response]},
        goto=cast(Literal["financial_statements_tool", "retriever_tool", "__end__"], node_name),
    )
