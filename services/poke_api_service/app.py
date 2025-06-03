from flask import Flask, request, jsonify
import time
from datetime import datetime
from poke_client import PokeApiClient
from logger import setup_logger


app = Flask(__name__)
logger = setup_logger()
poke_client = PokeApiClient()

@app.route('/health',methods=['GET'])
def health_check():
    """Health check endpoint para verificar disponibilidad del servicio"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|HEALTH|health_check Started")
        
        # Verificar si el servicio está funcionando
        response = {"status": "healthy", "service": "poke_api_service", "timestamp": datetime.now().isoformat()}
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)  # en milisegundos
        
        logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|HEALTH|health_check Completed - Latency: {latency}ms")
        
        return jsonify(response), 200
        
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_API_SERVICE|HEALTH|health_check Failed - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500
    
@app.route('/pokemon/<pokemon_name>', methods=['GET'])
def get_pokemon(pokemon_name):
    """Obtener información de un Pokémon desde PokeAPI"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon Started - Pokemon: {pokemon_name}")
        
        # Llamar al cliente de PokeAPI
        pokemon_data = poke_client.get_pokemon(pokemon_name.lower())
        
        if not pokemon_data:
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            logger.warning(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon Not Found - Pokemon: {pokemon_name} - Latency: {latency}ms")
            return jsonify({"error": "Pokemon not found"}), 404
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon Completed - Pokemon: {pokemon_name} - Latency: {latency}ms")
        
        return jsonify({
            "pokemon": pokemon_data,
            "source": "pokeapi",
            "latency_ms": latency,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon Failed - Pokemon: {pokemon_name} - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/pokemon/batch', methods=['POST'])
def get_pokemon_batch():
    """Obtener información de múltiples Pokémon (para testing de carga)"""
    start_time = time.time()
    try:
        data = request.get_json()
        pokemon_names = data.get('pokemon_names', [])
        
        logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_batch Started - Count: {len(pokemon_names)}")
        
        results = []
        for name in pokemon_names:
            pokemon_data = poke_client.get_pokemon_data(name.lower())
            if pokemon_data:
                results.append({
                    "name": name,
                    "data": pokemon_data,
                    "status": "success"
                })
            else:
                results.append({
                    "name": name,
                    "data": None,
                    "status": "not_found"
                })
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_batch Completed - Count: {len(pokemon_names)} - Latency: {latency}ms")
        
        return jsonify({
            "results": results,
            "total_processed": len(pokemon_names),
            "successful": len([r for r in results if r["status"] == "success"]),
            "latency_ms": latency,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_batch Failed - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|SYSTEM|startup Service starting on port 5001")
    app.run(host='0.0.0.0', port=5001, debug=True)

    