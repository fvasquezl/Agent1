# Agent1

Agente de chat en español para la terminal, construido sobre la API de [Groq](https://groq.com/) (compatible con OpenAI). El agente puede llamar herramientas (*tool calling*) y recuerda los últimos mensajes de la conversación.

Por ahora incluye una sola herramienta de ejemplo, `obtener_clima`, que devuelve respuestas fijas (no consulta ningún servicio real de clima).

## Requisitos

- Python 3.14
- Una API key de Groq ([console.groq.com/keys](https://console.groq.com/keys))

## Instalación

```bash
git clone https://github.com/fvasquezl/Agent1.git
cd Agent1
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz del proyecto con tu API key:

```
GROQ_API_KEY=tu_api_key
```

El archivo `.env` está en `.gitignore`, así que no se sube al repositorio.

## Uso

```bash
source env/bin/activate
python agent.py
```

Escribe tus mensajes después de `Tú:`. Para salir escribe `salir` o `exit`.

```
Agente de IA
Tú: ¿Cómo está el clima en Tijuana?
Herramienta obtener_clima llamada con Tijuana
Asistente: La temperatura actual en Tijuana es demasiado hermosa para ser verdad
Tú: ¿Y en Monterrey?
Herramienta obtener_clima llamada con Monterrey
Asistente: La temperatura actual en Monterrey es horripilante
Tú: salir
Hasta luego!
```

## Estructura

| Archivo | Descripción |
|---|---|
| `agent.py` | Ciclo de chat, prompt del sistema, definición de herramientas (`TOOLS`) y ciclo de llamadas a herramientas. Usa el modelo `openai/gpt-oss-120b`. |
| `tools.py` | Clase `Tools` con la implementación de las herramientas. |
| `simple_memory.py` | Memoria de conversación: guarda los últimos 10 mensajes (configurable con `MEMORY_MAX_MESSAGES` en `agent.py`). |

## Agregar una herramienta

1. Implementa el método en la clase `Tools` de `tools.py`.
2. Declara su esquema en la lista `TOOLS` de `agent.py`.
3. Agrega su rama en el `if/elif` de `process_response()` en `agent.py`.
4. Descríbela en `SYSTEM_PROMPT` para que el modelo sepa cuándo usarla.

Si falta el paso 3, el agente responde con el error "Herramienta desconocida".
