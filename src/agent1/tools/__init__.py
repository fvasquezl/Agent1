from agent1.tools import clima, tipo_cambio
from agent1.tools.base import Tool

# Para agregar una herramienta: crea su módulo con una lista TOOLS y agrégala aquí
ALL_TOOLS: list[Tool] = [*clima.TOOLS, *tipo_cambio.TOOLS]

__all__ = ["ALL_TOOLS", "Tool"]
