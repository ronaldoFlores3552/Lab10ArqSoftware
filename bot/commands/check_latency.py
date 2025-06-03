import requests
from datetime import datetime

SEARCH_API_BASE_URL = "http://localhost:5000"  # Ajustar si cambia

def check_latency(module='all'):
    """
    Ejecuta el comando CheckLatency consultando el microservicio search_api.
    Parámetros:
    - module: nombre del módulo para verificar latencia ('all' por defecto)
    Retorna:
    - Diccionario con resultados de latencia o error.
    """
    endpoint = f"{SEARCH_API_BASE_URL}/check_latency"
    params = {"module": module}

    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return {
            "success": True,
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
    except requests.RequestException as e:
        return {
            "success": False,
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }
