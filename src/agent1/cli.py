from groq import Groq

from agent1.agent import Agent
from agent1.config import MEMORY_MAX_MESSAGES, MODEL, groq_api_key
from agent1.memory import SimpleMemory
from agent1.tools import ALL_TOOLS


def main():
    agent = Agent(
        client=Groq(api_key=groq_api_key()),
        model=MODEL,
        tools=ALL_TOOLS,
        memory=SimpleMemory(max_messages=MEMORY_MAX_MESSAGES),
    )

    print("Agente de IA")
    while True:
        try:
            user_text = input("Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            user_text = "salir"
            print()

        if not user_text:
            continue
        if user_text.lower() in ("exit", "salir"):
            print("Hasta luego!")
            break

        print(f"Asistente: {agent.chat(user_text)}")
