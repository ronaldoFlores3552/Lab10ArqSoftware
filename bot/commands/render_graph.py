import requests
from datetime import datetime

SEARCH_API_BASE_URL = "http://localhost:5000"  # Ajustar si cambia

def render_graph(metric, module='all', period='Last5Days'):
    """
    Ejecuta el comando RenderGraph consultando el microservicio search_api.
    Parámetros:
    - metric: 'availability' o 'latency'
    - module: módulo a consultar ('all' por defecto)
    - period: período a consultar ('Last5Days' por defecto)
    Retorna:
    - Diccionario con datos para graficar o error.
    """
    endpoint = f"{SEARCH_API_BASE_URL}/render_graph"
    params = {
        "metric": metric,
        "module": module,
        "period": period
    }

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
