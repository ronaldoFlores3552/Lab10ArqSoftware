import logging
import os
from datetime import datetime

def setup_logger():
    """
    Configuracion logger standar para poke_api_service.
    Formato return: {Fecha}{Modulo}{API}{Funcion} Message
    """
    
    #creando directorio de logs si no existe 
    log_dir= os.path.join(os.path.dirname(__file__), 'logs','poke_api_service')
    os.makedirs(log_dir, exist_ok=True)
    
    #nombre archivo de log con fecha
    log_filename = f"poke_api_service_{datetime.now().strftime('%Y-%m-%d')}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    #configurando logger
    logger = logging.getLogger('poke_api_service')
    logger.setLevel(logging.INFO)
    
    #evitar duplicar handlers
    if logger.handlers:
        return logger
    
    #formato personalizado que sigue estandar requerido
    # formato: {Fecha}{Modulo}{API}{Funcion} Message
    class StandardFormatter(logging.Formatter):
        def format(self, record):
            #mensaje formateado
            return record.getMessage()
        
    #handler para archivo
    file_handler= logging.FileHandler(log_path,encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(StandardFormatter())
    
    #handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(StandardFormatter())
    
    #agregando handlers al logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger