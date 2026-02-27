"""Node: classifies email intent using an LLM."""
from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from agent.config import settings
from agent.state import EmailState

_SYSTEM = """\
You are a classifier for a garden store customer support system.
Given a customer email, respond with a JSON object with exactly two keys:
  - "intent": either "plant_instructions" (the customer is asking for plant care advice,
    planting instructions, watering, fertilising, pests, pruning, etc.)
    or "other" (anything else: orders, returns, complaints, general questions).
  - "topic": a short (≤10 words) description of the email subject.

Respond ONLY with the raw JSON object, no markdown fences.
"""

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _SYSTEM),
        ("human", "Email:\n\n{email_body}"),
    ]
)


def classifier_node(state: EmailState) -> dict:
    """Classify the email and return intent + topic."""
    if state.error:
        return {}

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )
    chain = _prompt | llm

    response = chain.invoke({"email_body": state.email_body})
    raw = response.content.strip()

    import json  # noqa: PLC0415

    try:
        data = json.loads(raw)
        intent = data.get("intent", "other")
        topic = data.get("topic", "")
    except json.JSONDecodeError:
        intent = "other"
        topic = "unknown"

    return {"intent": intent, "topic": topic}