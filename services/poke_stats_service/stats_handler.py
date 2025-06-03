import os
import time
import pandas as pd
from datetime import datetime
from logger import setup_logger

class StatsHandler:
    def __init__(self):
        """
        Inicializar StatsHandler con configuración de logger
        """
        self.logger = setup_logger()
        self.base_stats_path= os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'Poke_stats.csv'
        )
        self._dataframe = None
        
    def _load_stats(self):
        """Cargar el csv en un DataFrame de pandas, manejo errores y logging"""
        start_time = time.time()
        
        try:
            if not os.path.exists(self.base_stats_path):
                self.logger.error(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|FILE_NOT_FOUND|Path: {self.base_stats_path}")
                return None
            df = pd.read_csv(self.base_stats_path)
            self._dataframe = df
            end_time = time.time()
            latency = round((end_time - start_time)*1000, 2)
            self.logger.info(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|LOAD_STATS|Success loading CSV - Rows: {len(df)} - Latency: {latency}ms")
            return df
        except Exception as e:
            end_time = time.time()
            latency = round((end_time - start_time)*1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|LOAD_STATS|Error loading CSV - Latency: {latency}ms - Error: {str(e)}")
            return None
    def get_stats_dataframe(self):
        """Obtener DataFrame con todos los datos del CSV, cargar si no está ya cargado"""
        if self._dataframe is None:
            return self._load_stats()
        return self._dataframe
    def get_pokemon_stats(self, pokemon_name):
        """
        Filtrar el DataFrame para obtener estadísticas de un Pokémon específico.
        Se espera que el CSV tenga una columna con nombre 'pokemon' o similar (ajustar según CSV)
        """
        start_time = time.time()
        try:
            df = self.get_stats_dataframe()
            if df is None:
                return None

            # Normalizar a minúsculas para búsqueda case-insensitive
            normalized_name = pokemon_name.strip().lower()

            # Verificar que 'Name' está en columnas
            if 'Name' not in df.columns:
                self.logger.error(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_POKEMON_STATS|Column 'Name' not found in CSV")
                return None

            # Crear una columna temporal en minúsculas para comparación
            df['Name_lower'] = df['Name'].str.lower()

            filtered = df[df['Name_lower'] == normalized_name]

            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)

            if not filtered.empty:
                self.logger.info(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_POKEMON_STATS|Found stats for {pokemon_name} - Rows: {len(filtered)} - Latency: {latency}ms")
                # Opcional: eliminar la columna temporal antes de devolver
                filtered = filtered.drop(columns=['Name_lower'])
                return filtered
            else:
                self.logger.warning(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_POKEMON_STATS|No stats found for {pokemon_name} - Latency: {latency}ms")
                return None

        except Exception as e:
            end_time = time.time()
            latency = round((end_time - start_time) * 1000, 2)
            self.logger.error(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_POKEMON_STATS|Error - Pokemon: {pokemon_name} - Latency: {latency}ms - Error: {str(e)}")
            return None
    def get_all_pokemon_names(self):
        """
        Devuelve la lista única de nombres de Pokémon en el CSV 
        """
        try:
            df = self.get_stats_dataframe()
            if df is None or 'Name' not in df.columns:
                return []
            
            unique_names = df['Name'].dropna().unique().tolist()
            return unique_names
        
        except Exception as e:
            self.logger.error(f"{datetime.now().isoformat()}|POKE_STATS_SERVICE|GET_ALL_POKEMON_NAMES|Error: {str(e)}")
            return []
