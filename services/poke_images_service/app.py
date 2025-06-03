from flask import Flask, request, jsonify, send_file
import time
import os
from datetime import datetime
from image_handler import ImageHandler
from logger import setup_logger

app = Flask(__name__)
logger = setup_logger()
image_handler = ImageHandler()

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint para verificar disponibilidad del servicio"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|health_check Started")
        
        # Verificar si el directorio de imágenes existe
        images_dir = image_handler.get_images_base_path()
        if os.path.exists(images_dir):
            status = "healthy"
            message = f"Images directory accessible at {images_dir}"
        else:
            status = "unhealthy"
            message = f"Images directory not found at {images_dir}"
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        response = {
            "status": status,
            "service": "poke_images_service",
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        if status == "healthy":
            logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|health_check Completed - Latency: {latency}ms")
            return jsonify(response), 200
        else:
            logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|health_check Failed - Latency: {latency}ms - {message}")
            return jsonify(response), 500
            
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|health_check Failed - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/pokemon/<pokemon_name>/images', methods=['GET'])
def get_pokemon_images(pokemon_name):
    """Obtener lista de imágenes disponibles para un Pokémon"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_images Started - Pokemon: {pokemon_name}")
        
        images_info = image_handler.get_pokemon_images_info(pokemon_name)
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        if images_info:
            logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_images Completed - Pokemon: {pokemon_name} - Images: {len(images_info['images'])} - Latency: {latency}ms")
            
            return jsonify({
                "pokemon": pokemon_name,
                "images_info": images_info,
                "source": "local_files",
                "latency_ms": latency,
                "timestamp": datetime.now().isoformat()
            }), 200
        else:
            logger.warning(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_images Not Found - Pokemon: {pokemon_name} - Latency: {latency}ms")
            return jsonify({"error": f"No images found for pokemon: {pokemon_name}"}), 404
            
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_images Failed - Pokemon: {pokemon_name} - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/pokemon/<pokemon_name>/image/<image_name>', methods=['GET'])
def get_pokemon_image(pokemon_name, image_name):
    """Servir una imagen específica de un Pokémon"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_image Started - Pokemon: {pokemon_name} - Image: {image_name}")
        
        image_path = image_handler.get_pokemon_image_path(pokemon_name, image_name)
        
        if image_path and os.path.exists(image_path):
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            
            logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_image Completed - Pokemon: {pokemon_name} - Image: {image_name} - Latency: {latency}ms")
            
            return send_file(image_path)
        else:
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            
            logger.warning(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_image Not Found - Pokemon: {pokemon_name} - Image: {image_name} - Latency: {latency}ms")
            return jsonify({"error": f"Image not found: {image_name} for pokemon: {pokemon_name}"}), 404
            
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_image Failed - Pokemon: {pokemon_name} - Image: {image_name} - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/pokemon/<pokemon_name>/random-image', methods=['GET'])
def get_random_pokemon_image(pokemon_name):
    """Obtener una imagen aleatoria de un Pokémon"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_random_pokemon_image Started - Pokemon: {pokemon_name}")
        
        random_image_path = image_handler.get_random_pokemon_image(pokemon_name)
        
        if random_image_path and os.path.exists(random_image_path):
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            
            image_name = os.path.basename(random_image_path)
            logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_random_pokemon_image Completed - Pokemon: {pokemon_name} - Image: {image_name} - Latency: {latency}ms")
            
            return send_file(random_image_path)
        else:
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            
            logger.warning(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_random_pokemon_image Not Found - Pokemon: {pokemon_name} - Latency: {latency}ms")
            return jsonify({"error": f"No images found for pokemon: {pokemon_name}"}), 404
            
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_random_pokemon_image Failed - Pokemon: {pokemon_name} - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/pokemon/batch-images', methods=['POST'])
def get_batch_pokemon_images():
    """Obtener información de imágenes de múltiples Pokémon (para testing)"""
    start_time = time.time()
    try:
        data = request.get_json()
        pokemon_names = data.get('pokemon_names', [])
        
        logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_batch_pokemon_images Started - Count: {len(pokemon_names)}")
        
        results = []
        for name in pokemon_names:
            images_info = image_handler.get_pokemon_images_info(name)
            if images_info:
                results.append({
                    "name": name,
                    "images_info": images_info,
                    "status": "success"
                })
            else:
                results.append({
                    "name": name,
                    "images_info": None,
                    "status": "not_found"
                })
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_batch_pokemon_images Completed - Count: {len(pokemon_names)} - Latency: {latency}ms")
        
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
        logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_batch_pokemon_images Failed - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/available-pokemon', methods=['GET'])
def get_available_pokemon():
    """Obtener lista de Pokémon que tienen imágenes disponibles"""
    start_time = time.time()
    try:
        logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_available_pokemon Started")
        
        available_pokemon = image_handler.get_available_pokemon_list()
        
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        
        logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_available_pokemon Completed - Count: {len(available_pokemon)} - Latency: {latency}ms")
        
        return jsonify({
            "available_pokemon": available_pokemon,
            "total_count": len(available_pokemon),
            "latency_ms": latency,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        end_time = time.time()
        latency = round((end_time - start_time) * 1000, 2)
        logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_available_pokemon Failed - Latency: {latency}ms - Error: {str(e)}")
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|SYSTEM|startup Service starting on port 5003")
    app.run(host='0.0.0.0', port=5003, debug=True)