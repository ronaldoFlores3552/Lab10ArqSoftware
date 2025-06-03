import logging

def setup_logger():
    logger = logging.getLogger("search_api_service")
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s|SEARCH_API_SERVICE|API|%(funcName)s %(message)s', "%Y-%m-%dT%H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
