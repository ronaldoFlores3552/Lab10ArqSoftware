import logging
import os
from datetime import datetime

def setup_logger():
    """
    Configurar logger estándar para poke_stats_service
    Formato: {Fecha}{Modulo}{API}{Funcion} Message
    """
    
    # Crear directorio de logs si no existe
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'poke_stats_service')
    os.makedirs(log_dir, exist_ok=True)
    
    # Nombre del archivo de log con fecha
    log_filename = f"poke_stats_service_{datetime.now().strftime('%Y%m%d')}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    #configurar logger
    logger = logging.getLogger('poke_stats_service')
    logger.setLevel(logging.INFO)
    
    #evitar duplicar handlers si ya está configurado
    if logger.handlers:
        return logger
    
    # Formatter personalizado que sigue el estándar requerido
    # Formato: {Fecha}{Modulo}{API}{Funcion} Message
    class StandardFormatter(logging.Formatter):
        def format(self, record):
            # El mensaje ya viene formateado desde las funciones
            return record.getMessage()
    # Handler para archivo
    file_handler= logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(StandardFormatter())
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(StandardFormatter())
    
    # Añadir handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger