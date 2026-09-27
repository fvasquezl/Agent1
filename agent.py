import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from groq import Groq

from simple_memory import SimpleMemory
from tools import Tools

load_dotenv()


MEMORY_MAX_MESSAGES = 10

api_key = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key)
memory = SimpleMemory(max_messages=MEMORY_MAX_MESSAGES)
now = datetime.now(ZoneInfo("America/Tijuana"))
SYSTEM_PROMPT = """
Eres un asistente que habla en español y responde de manera muy breve y concisa.

Herramientas
- Cuentas con una herramienta llamada obtener clima, la cual te da el clima actual para cualquier ciudad
Al llamar a esta herramienta, la ciudad es obligatoria.
La respuesta que te dé esta herramienta debes regresarla tal cual, considerando que es correcta.
"""
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "obtener_clima",
            "description": (
                "Llama a esta funcion para obtener el clima actual en cualquier lugar. "
                "Se debe enviar como argumento el nombre de la ciudad de donde se desea obtener el clima "
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "La ciudad de la cual se desea obtener el clima",
                    },
                },
                "required": ["ciudad"],
            },
        },
    }
]

print("Agente de IA")


def process_response(client: Groq, memory_messages: list[dict], user_text: str):
    # Obtener la memoria
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(memory_messages)
    messages.append({"role": "user", "content": user_text})

    while True:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-120b", messages=messages, tools=TOOLS
        )

        msg = resp.choices[0].message

        # Si no hay llamados a herramientas, entonces ya regresamos la respuesta
        if not getattr(msg, "tool_calls", None):
            return msg.content or ""

        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": [tc.model_dump() for tc in msg.tool_calls],
            }
        )

        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments or "{}")

            if name == "obtener_clima":
                tools = Tools()
                result = tools.obtener_clima(ciudad=args["ciudad"])
            else:
                print(f"Se intentó llamar a una herramienta desconocida {name}")
                result = {"error": f"Herramienta desconocida: {name}"}

            # Agregar a los mensajes el resultao del llamado de la herramienta.
            # Esto lo recibirá el modelo al continuar la iteración
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False),
                }
            )


while True:
    user_text = input("Tú: ").strip()
    if not user_text:
        continue

    if user_text.lower() in ("exit", "salir"):
        print("Hasta luego!")
        break

    assistant_text = process_response(client, memory.messages(), user_text)
    print(f"Asistente: {assistant_text}")

    # Actualizar la memoria
    memory.add("user", user_text)
    memory.add("assistant", assistant_text)
