"""
Main module.
"""

import os
import json
from dataclasses import dataclass
import requests
from dotenv import load_dotenv

from chatgpt_client.config import (
    TIMEOUT,
)

load_dotenv()


@dataclass
class ChatGPTConfig:
    """
    Class defining the configuration for the
    ChatGPT Client.
    """

    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    api_url: str = "https://api.openai.com/v1/chat/completions"


class ChatGPTClient:
    """
    A simple ChatGPT client to interact with OpenAI's GPT API.
    """

    def __init__(self, config: ChatGPTConfig | None = None) -> None:
        """
        Initialize the ChatGPT client.
        :param config: ChatGPTConfig object containing API key, model, and temperature.
        """
        self.config = config or ChatGPTConfig()
        self.history: list[dict[str, str]] = []  # Store conversation history

    def send_message(self, message: str) -> str:
        """
        Send a message to ChatGPT and get a response.
        :param message: User input message.
        :return: ChatGPT's response.
        """
        self.history.append({"role": "user", "content": message})

        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.config.model,
            "messages": self.history,
            "temperature": self.config.temperature,
        }

        _response = requests.post(
            url=self.config.api_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )

        if _response.status_code == 200:
            reply = _response.json()["choices"][0]["message"]["content"]
            self.history.append({"role": "assistant", "content": reply})
            return reply

        return f"Error: {_response.status_code} - {_response.text}"

    def clear_history(self):
        """
        Clear the conversation history.
        """
        self.history = []


if __name__ == "__main__":

    client = ChatGPTClient()

    MESSAGE = "Hello World!"
    response = client.send_message(message=MESSAGE)
    print(response)
