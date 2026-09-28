import json

from groq import Groq
from groq.types.chat import ChatCompletionMessageParam

from agent1.memory import SimpleMemory
from agent1.tools import Tool

SYSTEM_PROMPT = """
Eres un asistente que habla en español y responde de manera muy breve y concisa.
Usa las herramientas disponibles cuando la pregunta lo requiera.
"""


class Agent:
    def __init__(
        self,
        client: Groq,
        model: str,
        tools: list[Tool],
        memory: SimpleMemory,
        system_prompt: str = SYSTEM_PROMPT,
    ):
        self.client = client
        self.model = model
        self.tools = {tool.name: tool for tool in tools}
        self.schemas = [tool.schema() for tool in tools]
        self.memory = memory
        self.system_prompt = system_prompt

    def chat(self, user_text: str) -> str:
        messages: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": self.system_prompt},
            *self.memory.messages(),
            {"role": "user", "content": user_text},
        ]

        while True:
            resp = self.client.chat.completions.create(
                model=self.model, messages=messages, tools=self.schemas
            )
            msg = resp.choices[0].message

            # Si no hay llamados a herramientas, ya tenemos la respuesta final
            if not msg.tool_calls:
                answer = msg.content or ""
                self.memory.add("user", user_text)
                self.memory.add("assistant", answer)
                return answer

            messages.append(
                {
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments,
                            },
                        }
                        for tc in msg.tool_calls
                    ],
                }
            )

            # El resultado de cada herramienta lo recibirá el modelo en la siguiente vuelta
            for tool_call in msg.tool_calls:
                result = self._run_tool(tool_call.function.name, tool_call.function.arguments)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": (
                            result
                            if isinstance(result, str)
                            else json.dumps(result, ensure_ascii=False)
                        ),
                    }
                )

    def _run_tool(self, name: str, arguments: str | None) -> object:
        tool = self.tools.get(name)
        if tool is None:
            print(f"Se intentó llamar a una herramienta desconocida {name}")
            return {"error": f"Herramienta desconocida: {name}"}

        try:
            return tool.func(**json.loads(arguments or "{}"))
        except (json.JSONDecodeError, TypeError) as e:
            return {"error": f"Argumentos inválidos para {name}: {e}"}
