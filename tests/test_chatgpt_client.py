"""
Test module.
"""

from unittest.mock import patch, MagicMock
import pytest
from chatgpt_client.client import (
    ChatGPTClient,
    ChatGPTConfig,
)


@pytest.fixture
def mock_config():
    """
    Fixture instancing a ChatGPTConfig object.
    """
    return ChatGPTConfig(api_key="test_api_key")


@pytest.fixture
def chatgpt_client(mock_config):
    """
    Fixture instancing a ChatGPTClient object.
    """
    return ChatGPTClient(config=mock_config)


@patch("requests.post")
def test_send_message(mock_post, chatgpt_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Hello from GPT!"}}]
    }
    mock_post.return_value = mock_response

    response = chatgpt_client.send_message("Hello")

    assert response == "Hello from GPT!"
    assert len(chatgpt_client.history) == 2
    assert chatgpt_client.history[0]["role"] == "user"
    assert chatgpt_client.history[1]["role"] == "assistant"


@patch("requests.post")
def test_send_message_error(mock_post, chatgpt_client):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_post.return_value = mock_response

    response = chatgpt_client.send_message("Hello")

    assert response == "Error: 400 - Bad Request"


def test_clear_history(chatgpt_client):
    chatgpt_client.history.append({"role": "user", "content": "Hello"})
    chatgpt_client.clear_history()
    assert len(chatgpt_client.history) == 0
