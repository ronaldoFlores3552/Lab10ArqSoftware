import requests
from datetime import datetime

SEARCH_API_BASE_URL = "http://localhost:5000"  # Ajustar si cambia

def check_availability(module='all'):
    """
    Ejecuta el comando CheckAvailability consultando el microservicio search_api.
    Parámetros:
    - module: nombre del módulo para verificar disponibilidad ('all' por defecto)
    Retorna:
    - Diccionario con resultados de disponibilidad o error.
    """
    endpoint = f"{SEARCH_API_BASE_URL}/check_availability"
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
