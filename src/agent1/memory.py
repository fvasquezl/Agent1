from collections import deque
from typing import Literal

from groq.types.chat import ChatCompletionMessageParam


class SimpleMemory:
    """Ventana deslizante con los últimos mensajes de la conversación."""

    def __init__(self, max_messages: int = 10):
        self.history: deque[ChatCompletionMessageParam] = deque(maxlen=max_messages)

    def add(self, role: Literal["user", "assistant"], text: str):
        if role == "user":
            self.history.append({"role": "user", "content": text})
        else:
            self.history.append({"role": "assistant", "content": text})

    def messages(self) -> list[ChatCompletionMessageParam]:
        return list(self.history)
