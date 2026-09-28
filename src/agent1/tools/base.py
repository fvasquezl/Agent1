from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from groq.types.chat import ChatCompletionToolParam


@dataclass(frozen=True)
class Tool:
    """Una herramienta: su esquema para el modelo y la función que la ejecuta."""

    name: str
    description: str
    parameters: dict[str, Any]
    func: Callable[..., Any]

    def schema(self) -> ChatCompletionToolParam:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }
