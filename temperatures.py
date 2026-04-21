import requests
import json
from datetime import datetime

LATITUD  = 41.3888
LONGITUD = 2.159

def obtenir_temperatures():
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude":      LATITUD,
        "longitude":     LONGITUD,
        "hourly":        "temperature_2m",
        "forecast_days": 1,
        "timezone":      "Europe/Madrid"
    }
    resposta = requests.get(url, params=params)
    resposta.raise_for_status()
    dades = resposta.json()
    return dades["hourly"]["temperature_2m"]

def calcular_estadistiques(temperatures):
    return {
        "maxima":  max(temperatures),
        "minima":  min(temperatures),
        "mitjana": round(sum(temperatures) / len(temperatures), 2)
    }

def exportar_json(temperatures, estadistiques):
    data_avui = datetime.now().strftime("%Y%m%d")
    nom_fitxer = f"temp_{data_avui}.json"
    contingut = {
        "data":          data_avui,
        "ciutat":        "Barcelona",
        "temperatures":  temperatures,
        "estadistiques": estadistiques
    }
    with open(nom_fitxer, "w") as f:
        json.dump(contingut, f, indent=2)
    print(f"Fitxer guardat: {nom_fitxer}")
    return nom_fitxer

if __name__ == "__main__":
    temps  = obtenir_temperatures()
    stats  = calcular_estadistiques(temps)
    fitxer = exportar_json(temps, stats)
    print(f"Màxima:  {stats['maxima']} °C")
    print(f"Mínima:  {stats['minima']} °C")
    print(f"Mitjana: {stats['mitjana']} °C")
