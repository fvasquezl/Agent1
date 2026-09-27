class Tools:
    def __init__(self):
        pass

    def obtener_clima(self, ciudad: str = ""):
        print(f"Herramienta obtener_clima llamada con {ciudad}")

        if ciudad.upper() == "TIJUANA":
            return f"La temperatura actual en {ciudad} es demasiado hermosa para ser verdad"
        else:
            return f"La temperatura actual en {ciudad} es horripilante"
