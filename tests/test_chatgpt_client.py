"""
Test module.
"""

from unittest.mock import patch, MagicMock
import pytest
import requests
from chatgpt_client.client import (
    ChatGPTClient,
    ChatGPTConfig,
)


@pytest.fixture
def mock_config() -> ChatGPTConfig:
    """
    Fixture instancing a ChatGPTConfig object.
    """
    return ChatGPTConfig(
        api_key="dummy_api_key",
        model="dummy_model",
        temperature=0.5,
        api_url="http://dummy.api",
    )


@pytest.fixture
def chatgpt_client(mock_config) -> ChatGPTClient:
    """
    Fixture instancing a ChatGPTClient object.
    """
    client_instance = ChatGPTClient(config=mock_config)
    client_instance.clear_history()
    return client_instance


@patch("requests.post")
def test_send_message_success(mock_post, chatgpt_client):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Hello from GPT!"}}]
    }
    mock_post.return_value = mock_response

    response = chatgpt_client.send_message("Hello")

    mock_response.raise_for_status.assert_called_once()

    assert response == "Hello from GPT!"
    assert len(chatgpt_client.history) == 2
    assert chatgpt_client.history[0]["role"] == "user"
    assert chatgpt_client.history[1]["role"] == "assistant"


def test_send_message_http_error(chatgpt_client, capsys):
    """
    Test that send_message handles HTTP errors gracefully.
    """
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"

    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Not Found"
    )

    with patch("requests.post", return_value=mock_response):
        reply = chatgpt_client.send_message("Test HTTP error")

    captured = capsys.readouterr().out
    assert "HTTP error occurred:" in captured
    assert reply is None


def test_send_message_connection_error(chatgpt_client, capsys):
    """
    Test that send_message handles connection errors gracefully.
    """
    with patch(
        "requests.post",
        side_effect=requests.exceptions.ConnectionError("Connection failed"),
    ):
        reply = chatgpt_client.send_message("Test connection error")

    captured = capsys.readouterr().out
    assert "Connection error occurred:" in captured
    assert "Connection failed" in captured
    assert reply is None


def test_send_message_timeout(chatgpt_client, capsys):
    """
    Test that send_message handles timeout errors gracefully.
    """
    with patch(
        "requests.post", side_effect=requests.exceptions.Timeout("Request timed out")
    ):
        reply = chatgpt_client.send_message("Test timeout error")

    captured = capsys.readouterr().out
    assert "Timeout error occurred:" in captured
    assert "Request timed out" in captured
    assert reply is None


def test_send_message_generic_error(chatgpt_client, capsys):
    """
    Test that send_message handles generic errors gracefully.
    """
    with patch(
        "requests.post",
        side_effect=requests.exceptions.RequestException("Generic error"),
    ):
        reply = chatgpt_client.send_message("Test generic error")

    captured = capsys.readouterr().out
    assert "An error occurred:" in captured
    assert "Generic error" in captured
    assert reply is None


def test_clear_history(chatgpt_client):
    # populate the history with dummy entries.
    chatgpt_client.history.append({"role": "user", "content": "Test Message"})
    chatgpt_client.history.append({"role": "assistant", "content": "Test Message"})
    chatgpt_client.clear_history()
    assert len(chatgpt_client.history) == 0
