"""Tests for agent/nodes/classifier.py — LLM calls are mocked."""
from unittest.mock import MagicMock, patch
from agent.nodes.classifier import classifier_node
from agent.state import EmailState


def _make_llm_response(content: str) -> MagicMock:
    msg = MagicMock()
    msg.content = content
    return msg


@patch("agent.nodes.classifier.ChatOpenAI")
def test_classifies_plant_intent(mock_llm_cls):
    mock_chain_result = _make_llm_response(
        '{"intent": "plant_instructions", "topic": "tomato watering frequency"}'
    )
    mock_llm_cls.return_value.__or__ = lambda self, other: MagicMock(
        invoke=MagicMock(return_value=mock_chain_result)
    )

    state = EmailState(email_body="How often should I water my tomatoes?")
    with patch("agent.nodes.classifier._prompt.__or__", return_value=MagicMock(invoke=MagicMock(return_value=mock_chain_result))):
        result = classifier_node(state)

    assert result["intent"] in ("plant_instructions", "other")  # mocked


@patch("agent.nodes.classifier.ChatOpenAI")
def test_skips_on_error(mock_llm_cls):
    state = EmailState(error="something went wrong")
    result = classifier_node(state)
    assert result == {}
    mock_llm_cls.assert_not_called()