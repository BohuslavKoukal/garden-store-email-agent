"""Node: generates a polite holding reply for non-plant emails."""
from __future__ import annotations

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from agent.config import settings
from agent.state import EmailState

_SYSTEM = """\
You are a customer service agent for an online garden store.
Write a short, warm, personalised reply telling the customer that their inquiry
has been received and that a human team member will get back to them soon.
Address the customer by name if known.
Do NOT attempt to resolve the issue — just acknowledge and reassure.
Keep it to 3–5 sentences.
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


def other_reply_node(state: EmailState) -> dict:
    """Generate a holding reply and mark it as the final answer (no approval needed)."""
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
    text = response.content.strip()
    return {"draft_answer": text, "final_answer": text, "approved": True}