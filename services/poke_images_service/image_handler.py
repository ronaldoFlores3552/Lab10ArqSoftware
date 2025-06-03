import os
import random
import time
from datetime import datetime
from logger import setup_logger

class ImageHandler:
    def __init__(self):
        self.logger = setup_logger()
        # Ruta base de las imágenes (desde la raíz del proyecto)
        self.base_images_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
            'data', 
            'Poke_Img'
        )
        self.supported_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        
    def get_images_base_path(self):
        """Obtener la ruta base del directorio de imágenes"""
        return self.base_images_path
    
    def _normalize_pokemon_name(self, pokemon_name):
        """Normalizar el nombre del Pokémon para búsqueda de carpetas"""
        # Capitalizar primera letra (ej: pikachu -> Pikachu)
        return pokemon_name.strip().capitalize()
    
    def _get_pokemon_directory(self, pokemon_name):
        """Obtener el directorio de un Pokémon específico"""
        normalized_name = self._normalize_pokemon_name(pokemon_name)
        pokemon_dir = os.path.join(self.base_images_path, normalized_name)
        return pokemon_dir if os.path.exists(pokemon_dir) else None
    
    def _get_image_files(self, directory_path):
        """Obtener lista de archivos de imagen en un directorio"""
        start_time = time.time()
        
        try:
            if not os.path.exists(directory_path):
                return []
            
            image_files = []
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    # Verificar extensión
                    _, ext = os.path.splitext(filename.lower())
                    if ext in self.supported_extensions:
                        # Obtener información del archivo
                        file_stats = os.stat(file_path)
                        image_files.append({
                            "filename": filename,
                            "path": file_path,
                            "size_bytes": file_stats.st_size,
                            "modified_date": datetime.fromtimestamp(file_stats.st_mtime).isoformat()
                        })
            
            end_time = time.time()
            scan_latency = round((end_time - start_time) * 1000, 2)
            
            self.logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|_get_image_files Scanned directory - Path: {directory_path} - Files: {len(image_files)} - Scan Latency: {scan_latency}ms")
            
            return image_files
            
        except Exception as e:
            end_time = time.time()
            scan_latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|_get_image_files Error scanning directory - Path: {directory_path} - Scan Latency: {scan_latency}ms - Error: {str(e)}")
            return []
    
    def get_pokemon_images_info(self, pokemon_name):
        """Obtener información de todas las imágenes de un Pokémon"""
        start_time = time.time()
        
        try:
            pokemon_dir = self._get_pokemon_directory(pokemon_name)
            
            if not pokemon_dir:
                end_time = time.time()
                latency = round((end_time - start_time) * 1000, 2)
                self.logger.warning(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_images_info Directory not found - Pokemon: {pokemon_name} - Latency: {latency}ms")
                return None
            
            image_files = self._get_image_files(pokemon_dir)
            
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            
            if image_files:
                result = {
                    "pokemon_name": pokemon_name,
                    "directory_path": pokemon_dir,
                    "images_count": len(image_files),
                    "images": image_files,
                    "total_size_bytes": sum(img["size_bytes"] for img in image_files)
                }
                
                self.logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_images_info Success - Pokemon: {pokemon_name} - Images: {len(image_files)} - Latency: {latency}ms")
                return result
            else:
                self.logger.warning(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_images_info No images found - Pokemon: {pokemon_name} - Latency: {latency}ms")
                return None
                
        except Exception as e:
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_images_info Error - Pokemon: {pokemon_name} - Latency: {latency}ms - Error: {str(e)}")
            return None
    
    def get_pokemon_image_path(self, pokemon_name, image_name):
        """Obtener la ruta completa de una imagen específica"""
        start_time = time.time()
        
        try:
            pokemon_dir = self._get_pokemon_directory(pokemon_name)
            
            if not pokemon_dir:
                end_time = time.time()
                latency = round((end_time - start_time) * 1000, 2)
                self.logger.warning(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_image_path Directory not found - Pokemon: {pokemon_name} - Image: {image_name} - Latency: {latency}ms")
                return None
            
            image_path = os.path.join(pokemon_dir, image_name)
            
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            
            if os.path.exists(image_path) and os.path.isfile(image_path):
                self.logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_image_path Success - Pokemon: {pokemon_name} - Image: {image_name} - Latency: {latency}ms")
                return image_path
            else:
                self.logger.warning(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_image_path File not found - Pokemon: {pokemon_name} - Image: {image_name} - Latency: {latency}ms")
                return None
                
        except Exception as e:
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_pokemon_image_path Error - Pokemon: {pokemon_name} - Image: {image_name} - Latency: {latency}ms - Error: {str(e)}")
            return None
    
    def get_random_pokemon_image(self, pokemon_name):
        """Obtener una imagen aleatoria de un Pokémon"""
        start_time = time.time()
        
        try:
            pokemon_dir = self._get_pokemon_directory(pokemon_name)
            
            if not pokemon_dir:
                end_time = time.time()
                latency = round((end_time - start_time) * 1000, 2)
                self.logger.warning(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_random_pokemon_image Directory not found - Pokemon: {pokemon_name} - Latency: {latency}ms")
                return None
            
            image_files = self._get_image_files(pokemon_dir)
            
            if not image_files:
                end_time = time.time()
                latency = round((end_time - start_time) * 1000, 2)
                self.logger.warning(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_random_pokemon_image No images found - Pokemon: {pokemon_name} - Latency: {latency}ms")
                return None
            
            # Seleccionar imagen aleatoria
            random_image = random.choice(image_files)
            
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            
            self.logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_random_pokemon_image Success - Pokemon: {pokemon_name} - Selected: {random_image['filename']} - Latency: {latency}ms")
            
            return random_image["path"]
            
        except Exception as e:
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_random_pokemon_image Error - Pokemon: {pokemon_name} - Latency: {latency}ms - Error: {str(e)}")
            return None
    
    def get_available_pokemon_list(self):
        """Obtener lista de Pokémon que tienen carpetas de imágenes"""
        start_time = time.time()
        
        try:
            if not os.path.exists(self.base_images_path):
                end_time = time.time()
                latency = round((end_time - start_time) * 1000, 2)
                self.logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_available_pokemon_list Base directory not found - Path: {self.base_images_path} - Latency: {latency}ms")
                return []
            
            pokemon_list = []
            for item in os.listdir(self.base_images_path):
                item_path = os.path.join(self.base_images_path, item)
                if os.path.isdir(item_path):
                    # Verificar si tiene imágenes
                    image_files = self._get_image_files(item_path)
                    if image_files:
                        pokemon_list.append({
                            "name": item,
                            "images_count": len(image_files),
                            "directory_path": item_path
                        })
            
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            
            self.logger.info(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_available_pokemon_list Success - Pokemon count: {len(pokemon_list)} - Latency: {latency}ms")
            
            return pokemon_list
            
        except Exception as e:
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_IMAGES_SERVICE|LOCAL_FILES|get_available_pokemon_list Error - Latency: {latency}ms - Error: {str(e)}")
            return []