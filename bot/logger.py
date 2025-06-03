import logging

def setup_logger():
    logger = logging.getLogger("bot")
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s|BOT|%(funcName)s %(message)s', "%Y-%m-%dT%H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
