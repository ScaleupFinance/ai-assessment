"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode

from agent.node import chat, finance, router
from agent.state import InputState, State
from agent.tools import financial_statements_tool, retriever_tool

# Define the graph
workflow = StateGraph(State, input_schema=InputState)

workflow.add_node("router", router)
workflow.add_node("chat", chat)
workflow.add_node("finance", finance)
workflow.add_node(
    "financial_statements_tool",
    ToolNode(
        [financial_statements_tool],
        messages_key="finance_messages",
    ),
)
workflow.add_node(
    "retriever_tool",
    ToolNode(
        [retriever_tool],
        messages_key="finance_messages",
    ),
)

workflow.add_edge("__start__", "router")
workflow.add_edge("financial_statements_tool", "finance")
workflow.add_edge("retriever_tool", "finance")

graph = workflow.compile()
graph.name = "AI_CFO"
