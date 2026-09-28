from typing import Any

import requests

from agent1.tools.base import Tool


def obtener_tipo_cambio(moneda: str) -> dict[str, Any] | str:
    print(f"Herramienta obtener_tipo_cambio llamada con {moneda}")
    if not moneda:
        return "ERROR: Es necesario indicar la moneda para obtener el tipo de cambio"

    try:
        response = requests.get(f"https://open.er-api.com/v6/latest/{moneda.upper()}", timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error en obtener_tipo_cambio con {moneda}", e)
        return f"ERROR: No fue posible obtener el tipo de cambio para la moneda {moneda}"


TOOLS = [
    Tool(
        name="obtener_tipo_cambio",
        description=(
            "Obtiene el tipo de cambio de una moneda frente a todas las demás. "
            "La moneda se indica en formato ISO 4217 (por ejemplo USD, MXN, EUR)."
        ),
        parameters={
            "type": "object",
            "properties": {
                "moneda": {
                    "type": "string",
                    "description": "Código ISO 4217 de la moneda base",
                },
            },
            "required": ["moneda"],
        },
        func=obtener_tipo_cambio,
    ),
]
