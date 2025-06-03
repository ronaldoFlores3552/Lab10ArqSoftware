from flask import Flask, request, jsonify
import time
import os
from datetime import datetime
from stats_handler import StatsHandler
from logger import setup_logger

app = Flask(__name__)
logger = setup_logger()
stats_handler = StatsHandler()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para verificar disponibilidad del servicio"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|HEALTH_CHECK Started")
        
        # Verificar si el archivo CSV existe
        stats_path = stats_handler.base_stats_path
        if os.path.exists(stats_path):
            status = "healthy"
            message = f"Stats CSV accessible at {stats_path}"
        else:
            status = "unhealthy"
            message = f"Stats CSV not found at {stats_path}"
        
        end_time = time.time()
        latency = round((end_time - start_time)*1000, 2)
        
        response = {
            "status": status,
            "service": "poke_stats_service",
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        if status == "healthy":
            logger.info(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|HEALTH_CHECK Completed - Latency: {latency}ms")
            return jsonify(response), 200
        else:
            logger.error(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|HEALTH_CHECK Failed - Latency: {latency}ms - {message}")
            return jsonify(response), 500
    
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time)*1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|HEALTH_CHECK Failed - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/pokemon/<pokemon_name>/stats', methods=['GET'])
def get_pokemon_stats(pokemon_name):
    """Obtener estadísticas de un Pokémon específico"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_POKEMON_STATS Started - Pokemon: {pokemon_name}")
        
        stats_df = stats_handler.get_pokemon_stats(pokemon_name)
        
        end_time = time.time()
        latency = round((end_time - start_time)*1000, 2)
        
        if stats_df is not None and not stats_df.empty:
            # Convertir DataFrame a lista de dicts para JSON
            stats_json = stats_df.to_dict(orient='records')
            
            logger.info(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_POKEMON_STATS Completed - Pokemon: {pokemon_name} - Rows: {len(stats_json)} - Latency: {latency}ms")
            
            return jsonify({
                "pokemon": pokemon_name,
                "stats": stats_json,
                "source": "poke_stats_csv",
                "latency_ms": latency,
                "timestamp": datetime.now().isoformat()
            }), 200
        else:
            logger.warning(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_POKEMON_STATS Not Found - Pokemon: {pokemon_name} - Latency: {latency}ms")
            return jsonify({"error": f"No stats found for pokemon: {pokemon_name}"}), 404
    
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time)*1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_POKEMON_STATS Failed - Pokemon: {pokemon_name} - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/available-pokemon', methods=['GET'])
def get_available_pokemon():
    """Obtener lista de nombres de Pokémon con estadísticas disponibles"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_AVAILABLE_POKEMON Started")
        
        pokemon_names = stats_handler.get_all_pokemon_names()
        
        end_time = time.time()
        latency = round((end_time - start_time)*1000, 2)
        
        logger.info(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_AVAILABLE_POKEMON Completed - Count: {len(pokemon_names)} - Latency: {latency}ms")
        
        return jsonify({
            "available_pokemon": pokemon_names,
            "total_count": len(pokemon_names),
            "latency_ms": latency,
            "timestamp": datetime.now().isoformat()
        }), 200
    
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time)*1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_AVAILABLE_POKEMON Failed - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    logger.info(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|SYSTEM|startup Service starting on port 5002")
    app.run(host='0.0.0.0', port=5002, debug=True)
