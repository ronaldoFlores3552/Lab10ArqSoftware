from flask import Blueprint, request, jsonify
from datetime import datetime
import time
import requests
from logger import setup_logger

logger = setup_logger()
bp = Blueprint('search_api', __name__)

# URLs base para microservicios monitoreados
POKE_API_URL = "http://localhost:5001"
POKE_STATS_URL = "http://localhost:5002"
POKE_IMAGES_URL = "http://localhost:5003"

def measure_latency(url, endpoint):
    full_url = f"{url}{endpoint}"
    start = time.time()
    try:
        resp = requests.get(full_url, timeout=5)
        latency_ms = round((time.time() - start) * 1000, 2)
        logger.info(f"Request to {full_url} status: {resp.status_code}, latency: {latency_ms}ms")
        return resp.status_code, latency_ms, resp.json() if resp.ok else None
    except requests.RequestException as e:
        latency_ms = round((time.time() - start) * 1000, 2)
        logger.error(f"Request to {full_url} failed after {latency_ms}ms: {str(e)}")
        return None, latency_ms, None

@bp.route('/check_latency', methods=['GET'])
def check_latency():
    module = request.args.get('module', 'all').lower()
    start_time = time.time()
    logger.info(f"Started latency check for module: {module}")

    results = {}
    targets = []
    if module == 'all':
        targets = [
            ("poke_api", POKE_API_URL),
            ("poke_stats", POKE_STATS_URL),
            ("poke_images", POKE_IMAGES_URL),
        ]
    elif module in ['poke_api', 'poke_stats', 'poke_images']:
        url_map = {
            "poke_api": POKE_API_URL,
            "poke_stats": POKE_STATS_URL,
            "poke_images": POKE_IMAGES_URL,
        }
        targets = [(module, url_map[module])]
    else:
        logger.warning(f"Invalid module param: {module}")
        return jsonify({"error": "Invalid module parameter"}), 400

    for mod_name, base_url in targets:
        status, latency_ms, _ = measure_latency(base_url, '/health')
        results[mod_name] = {
            "status_code": status,
            "latency_ms": latency_ms
        }

    total_latency = round((time.time() - start_time) * 1000, 2)
    logger.info(f"Completed latency check for module: {module} total_latency: {total_latency}ms")

    return jsonify({
        "module": module,
        "results": results,
        "total_latency_ms": total_latency,
        "timestamp": datetime.now().isoformat()
    })
@bp.route('/render_graph', methods=['GET'])
def render_graph():
    """
    Endpoint para renderizar datos para gráficos (simulados).
    Parámetros query:
    - metric: 'availability' o 'latency'
    - module: 'poke_api', 'poke_stats', 'poke_images' o 'all'
    - period: 'Last5Days' o 'Last7Days'
    """
    metric = request.args.get('metric', '').lower()
    module = request.args.get('module', 'all').lower()
    period = request.args.get('period', 'Last5Days').lower()

    logger.info(f"Render graph request metric={metric}, module={module}, period={period}")

    # Validaciones básicas
    if metric not in ['availability', 'latency']:
        return jsonify({"error": "Invalid metric parameter"}), 400
    if module not in ['poke_api', 'poke_stats', 'poke_images', 'all']:
        return jsonify({"error": "Invalid module parameter"}), 400
    if period not in ['last5days', 'last7days']:
        return jsonify({"error": "Invalid period parameter"}), 400

    # Datos simulados para respuesta
    mock_data = {
        "last5days": [95, 96, 97, 95, 94] if metric == "availability" else [120, 110, 130, 115, 125],
        "last7days": [94, 95, 96, 95, 93, 94, 92] if metric == "availability" else [125, 120, 130, 115, 135, 125, 140],
    }

    data = mock_data.get(period, [])

    response = {
        "metric": metric,
        "module": module,
        "period": period,
        "data": data,
        "timestamp": datetime.now().isoformat()
    }

    return jsonify(response)
@bp.route('/check_availability', methods=['GET'])
def check_availability():
    module = request.args.get('module', 'all').lower()
    start_time = time.time()
    logger.info(f"Started availability check for module: {module}")

    results = {}
    targets = []
    if module == 'all':
        targets = [
            ("poke_api", POKE_API_URL),
            ("poke_stats", POKE_STATS_URL),
            ("poke_images", POKE_IMAGES_URL),
        ]
    elif module in ['poke_api', 'poke_stats', 'poke_images']:
        url_map = {
            "poke_api": POKE_API_URL,
            "poke_stats": POKE_STATS_URL,
            "poke_images": POKE_IMAGES_URL,
        }
        targets = [(module, url_map[module])]
    else:
        logger.warning(f"Invalid module param: {module}")
        return jsonify({"error": "Invalid module parameter"}), 400

    for mod_name, base_url in targets:
        try:
            resp = requests.get(f"{base_url}/health", timeout=5)
            available = resp.status_code == 200
        except requests.RequestException:
            available = False
        results[mod_name] = available

    total_latency = round((time.time() - start_time) * 1000, 2)
    logger.info(f"Completed availability check for module: {module} total_latency: {total_latency}ms")

    return jsonify({
        "module": module,
        "availability": results,
        "total_latency_ms": total_latency,
        "timestamp": datetime.now().isoformat()
    })

# Similar para /check_availability y /render_graph ...
