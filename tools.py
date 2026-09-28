import requests


class Tools:
    def __init__(self):
        pass

    def obtener_clima(self, ciudad: str = ""):
        print(f"Herramienta obtener_clima llamada con {ciudad}")

        if ciudad.upper() == "TIJUANA":
            return f"La temperatura actual en {ciudad} es demasiado hermosa para ser verdad"
        else:
            return f"La temperatura actual en {ciudad} es horripilante"

    def obtener_clima_api(self, lat: str, long: str):
        print(f"Herramienta para obtener_clima_api llamada con {lat} y {long}")
        if not lat or not long:
            return "Error: Es necesario indicar la latitud y la longitud para obtener el clima"

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current_weather=true"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"Error al obtener_clima_api con {lat}, {long}", e)
            return f"ERROR: No fue posible obtener el clima para {lat}, {long}"

    def obtener_lat_long(self, ciudad: str = ""):
        print(f"Herramienta para obtener_lat_long llamada con {ciudad}")
        if not ciudad:
            return "Error: Es necesario indicar la ciudad para obtener su latitud y la longitud"

        url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1&language=es&format=json"
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.json()

        except Exception as e:
            print(f"Error al obtener_clima_api con {ciudad}", e)
            return f"ERROR: No fue posible obtener el clima para la ciudad {ciudad}"
