"""Node: generates a detailed plant-care answer."""
from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from agent.config import settings
from agent.state import EmailState

_SYSTEM = """\
You are a friendly and knowledgeable garden expert working for an online garden store.
Write a helpful, personalised reply to the customer's question about plants.
Address the customer by name if known.
Keep the tone warm, professional, and practical.
Limit the reply to ~200 words.
"""

_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", _SYSTEM),
        (
            "human",
            "Customer name: {sender_name}\n\nCustomer email:\n{email_body}",
        ),
    ]
)


def plant_advisor_node(state: EmailState) -> dict:
    """Generate a plant-care draft answer."""
    if state.error:
        return {}

    llm = ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.7,
    )
    chain = _prompt | llm
    response = chain.invoke(
        {"sender_name": state.sender_name, "email_body": state.email_body}
    )
    return {"draft_answer": response.content.strip()}