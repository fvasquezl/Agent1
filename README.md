# Agent1

Agente de chat en español para la terminal, construido sobre la API de [Groq](https://groq.com/) (compatible con OpenAI). El agente puede llamar herramientas (*tool calling*) y recuerda los últimos mensajes de la conversación.

Herramientas incluidas (usan APIs públicas, sin API key):

| Herramienta | Qué hace | API |
|---|---|---|
| `obtener_lat_long` | Latitud y longitud de una ciudad | [Open-Meteo Geocoding](https://open-meteo.com/en/docs/geocoding-api) |
| `obtener_clima_api` | Clima actual en unas coordenadas | [Open-Meteo](https://open-meteo.com/) |
| `obtener_tipo_cambio` | Tipo de cambio de una moneda (ISO 4217) | [ExchangeRate-API](https://www.exchangerate-api.com/docs/free) |

## Requisitos

- Python 3.14
- Una API key de Groq ([console.groq.com/keys](https://console.groq.com/keys))

## Instalación

```bash
git clone https://github.com/fvasquezl/Agent1.git
cd Agent1
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt   # versiones exactas probadas
pip install -e .                  # instala el paquete agent1 en modo editable
```

Crea un archivo `.env` en la raíz del proyecto con tu API key:

```
GROQ_API_KEY=tu_api_key
```

El archivo `.env` está en `.gitignore`, así que no se sube al repositorio.

## Uso

```bash
source venv/bin/activate
agent1            # o: python -m agent1
```

Escribe tus mensajes después de `Tú:`. Para salir escribe `salir` o `exit` (o `Ctrl+C`).

```
Agente de IA
Tú: ¿Qué clima hace en Tijuana y cuántos pesos mexicanos vale un dólar?
Herramienta obtener_lat_long llamada con Tijuana
Herramienta obtener_clima_api llamada con 32.5027 y -117.00371
Herramienta obtener_tipo_cambio llamada con USD
Asistente: En Tijuana: 26 °C, viento 13 km/h, cielo claro.
1 USD ≈ 17.74 MXN.
Tú: salir
Hasta luego!
```

## Estructura

```
src/agent1/
├── __main__.py        # permite `python -m agent1`
├── cli.py             # bucle "Tú: / Asistente:" (comando `agent1`)
├── config.py          # carga .env, modelo y tamaño de memoria
├── agent.py           # clase Agent: ciclo de tool calling
├── memory.py          # memoria de los últimos N mensajes
└── tools/
    ├── __init__.py    # ALL_TOOLS: registro de herramientas
    ├── base.py        # dataclass Tool (esquema + función)
    ├── clima.py
    └── tipo_cambio.py
```

## Agregar una herramienta

1. Crea un módulo en `src/agent1/tools/` con la función y una lista `TOOLS` de objetos `Tool` (nombre, descripción, parámetros JSON Schema y la función).
2. Agrega su `TOOLS` a `ALL_TOOLS` en `src/agent1/tools/__init__.py`.

El agente arma los esquemas y despacha las llamadas a partir de ese registro; no hay que tocar `agent.py`.
