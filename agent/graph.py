"""Wires all nodes into the LangGraph StateGraph."""
from __future__ import annotations

from langgraph.graph import StateGraph, END
from langgraph.graph.graph import CompiledStateGraph

from agent.state import EmailState
from agent.nodes.reader import reader_node
from agent.nodes.classifier import classifier_node
from agent.nodes.plant_advisor import plant_advisor_node
from agent.nodes.other_reply import other_reply_node
from agent.nodes.human_approval import human_approval_node
from agent.nodes.save_answer import save_answer_node


def _route_by_intent(state: EmailState) -> str:
    """Conditional edge: route based on classified intent."""
    if state.error:
        return END
    if state.intent == "plant_instructions":
        return "plant_advisor"
    return "other_reply"


def build_graph(interrupt_before_approval: bool = False) -> CompiledStateGraph:
    """
    Build and compile the email-processing graph.

    Args:
        interrupt_before_approval: When True (Streamlit mode), the graph
            pauses at 'human_approval' so the UI can collect input.
    """
    builder = StateGraph(EmailState)

    # Register nodes
    builder.add_node("reader", reader_node)
    builder.add_node("classifier", classifier_node)
    builder.add_node("plant_advisor", plant_advisor_node)
    builder.add_node("other_reply", other_reply_node)
    builder.add_node("human_approval", human_approval_node)
    builder.add_node("save_answer", save_answer_node)

    # Entry point
    builder.set_entry_point("reader")

    # Linear edges
    builder.add_edge("reader", "classifier")

    # Conditional routing after classification
    builder.add_conditional_edges(
        "classifier",
        _route_by_intent,
        {
            "plant_advisor": "plant_advisor",
            "other_reply": "other_reply",
            END: END,
        },
    )

    # Plant path → approval → save
    builder.add_edge("plant_advisor", "human_approval")
    builder.add_edge("human_approval", "save_answer")
    builder.add_edge("save_answer", END)

    # Other path → save directly (approved flag already set True in other_reply)
    builder.add_edge("other_reply", "save_answer")

    if interrupt_before_approval:
        return builder.compile(interrupt_before=["human_approval"])
    return builder.compile()