import os
import requests
import json
from dataclasses import dataclass
from dotenv import load_dotenv

from chatgpt_client.config import (
    TIMEOUT,
)

load_dotenv()


@dataclass
class ChatGPTConfig:
    api_key: str = os.getenv("OPENAI_API_KEY", "")
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    api_url: str = "https://api.openai.com/v1/chat/completions"


class ChatGPTClient:
    """
    A simple ChatGPT client to interact with OpenAI's GPT API.
    """

    def __init__(self, config: ChatGPTConfig = None) -> None:
        """
        Initialize the ChatGPT client.
        :param config: ChatGPTConfig object containing API key, model, and temperature.
        """
        self.config = config or ChatGPTConfig()
        self.history = []  # Store conversation history

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

        response = requests.post(
            url=self.config.api_url,
            headers=headers,
            data=json.dumps(payload),
            timeout=TIMEOUT,
        )

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            self.history.append({"role": "assistant", "content": reply})
            return reply
        else:
            return f"Error: {response.status_code} - {response.text}"

    def clear_history(self):
        """
        Clear the conversation history.
        """
        self.history = []


if __name__ == "__main__":

    config = ChatGPTConfig()
    client = ChatGPTClient()

    message = "Hello World!"
    response = client.send_message(message)
    print(response)
