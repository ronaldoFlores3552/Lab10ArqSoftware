import requests
import time
from datetime import datetime
from logger import setup_logger

class PokeApiClient:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2/pokemon"
        self.timeout = 30  # Timeout in seconds
        self.logger = setup_logger()
        
    def get_pokemon(self, pokemon_name):
        """Obtener datos de pokemon desde PokeApi externa"""
        
        start_time= time.time()
        url= f"{self.base_url}/{pokemon_name.lower()}"
        try:
            self.logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_data Started - URL: {url}")
            
            #realizar peticion http
            response = requests.get(url, timeout=self.timeout)
            end_time = time.time()
            api_latency=round((end_time - start_time)*1000, 2)
            if response.status_code == 200:
                data= response.json()
                
                #extraer infor relevante
                pokemon_info = {
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "height": data.get("height"),
                    "weight": data.get("weight"),
                    "base_experience": data.get("base_experience"),
                    "types": [type_info["type"]["name"] for type_info in data.get("types", [])],
                    "abilities": [ability["ability"]["name"] for ability in data.get("abilities", [])],
                    "stats": {
                        stat["stat"]["name"]: stat["base_stat"] 
                        for stat in data.get("stats", [])
                    },
                    "sprites": {
                        "front_default": data.get("sprites", {}).get("front_default"),
                        "back_default": data.get("sprites", {}).get("back_default")
                    }
                }
                self.logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_data Success - Pokemon: {pokemon_name} - API Latency: {api_latency}ms")
                return pokemon_info 
            elif response.status_code == 404:
                self.logger.warning(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_data Not Found - Pokemon: {pokemon_name} - API Latency: {api_latency}ms")
                return None
            else:
                self.logger.error(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_data HTTP Error - Pokemon: {pokemon_name} - Status: {response.status_code} - API Latency: {api_latency}ms")
                return None
        except requests.exceptions.ConnectionError as e:
            end_time = time.time()
            api_latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_data Connection Error - Pokemon: {pokemon_name} - API Latency: {api_latency}ms")
            return None
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            api_latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_data Request Error - Pokemon: {pokemon_name} - API Latency: {api_latency}ms - Error: {str(e)}")
            return None            
        except Exception as e:
            end_time = time.time()
            api_latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|get_pokemon_data Unexpected Error - Pokemon: {pokemon_name} - API Latency: {api_latency}ms - Error: {str(e)}")
            return None

    def health_check(self):
        """Realizar un health check a la PokeApi externa"""
        
        start_time = time.time()
        try:
            # Hacer una petición simple para verificar conectividad
            response = requests.get(f"{self.base_url}/1", timeout=10)  # Bulbasaur siempre existe
            
            end_time = time.time()
            api_latency = round((end_time - start_time) * 1000, 2)
            
            if response.status_code == 200:
                self.logger.info(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|health_check Success - API Latency: {api_latency}ms")
                return True, api_latency
            else:
                self.logger.error(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|health_check Failed - Status: {response.status_code} - API Latency: {api_latency}ms")
                return False, api_latency
        except requests.exceptions.RequestException as e:
            end_time = time.time()
            api_latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_API_SERVICE|EXTERNAL_API|health_check Error - API Latency: {api_latency}ms - Error: {str(e)}")
            return False, api_latency                            