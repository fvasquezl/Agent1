import os

from dotenv import load_dotenv

# Busca el .env subiendo desde este archivo, así funciona desde cualquier carpeta
load_dotenv()

MODEL = "openai/gpt-oss-120b"
MEMORY_MAX_MESSAGES = 10


def groq_api_key() -> str:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise SystemExit("Falta GROQ_API_KEY: agrégala al archivo .env")
    return api_key
