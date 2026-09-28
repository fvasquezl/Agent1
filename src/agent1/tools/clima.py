from typing import Any

import requests

from agent1.tools.base import Tool


def obtener_lat_long(ciudad: str) -> dict[str, Any] | str:
    print(f"Herramienta obtener_lat_long llamada con {ciudad}")
    if not ciudad:
        return "ERROR: Es necesario indicar la ciudad para obtener su latitud y longitud"

    try:
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": ciudad, "count": 1, "language": "es", "format": "json"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"Error en obtener_lat_long con {ciudad}", e)
        return f"ERROR: No fue posible obtener la latitud y longitud de {ciudad}"

    # Si no encuentra la ciudad, Open-Meteo responde sin "results"
    if not data.get("results"):
        return f"ERROR: No se encontró la ciudad {ciudad}"
    return data["results"][0]


def obtener_clima_api(lat: str, long: str) -> dict[str, Any] | str:
    print(f"Herramienta obtener_clima_api llamada con {lat} y {long}")
    if not lat or not long:
        return "ERROR: Es necesario indicar la latitud y la longitud para obtener el clima"

    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lat, "longitude": long, "current_weather": "true"},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error en obtener_clima_api con {lat}, {long}", e)
        return f"ERROR: No fue posible obtener el clima para {lat}, {long}"


TOOLS = [
    Tool(
        name="obtener_lat_long",
        description=(
            "Obtiene la latitud y longitud de una ciudad. "
            "Úsala antes de obtener_clima_api cuando solo conoces el nombre de la ciudad."
        ),
        parameters={
            "type": "object",
            "properties": {
                "ciudad": {
                    "type": "string",
                    "description": "Nombre de la ciudad",
                },
            },
            "required": ["ciudad"],
        },
        func=obtener_lat_long,
    ),
    Tool(
        name="obtener_clima_api",
        description="Obtiene el clima actual en una latitud y longitud.",
        parameters={
            "type": "object",
            "properties": {
                "lat": {"type": "string", "description": "Latitud del lugar"},
                "long": {"type": "string", "description": "Longitud del lugar"},
            },
            "required": ["lat", "long"],
        },
        func=obtener_clima_api,
    ),
]
