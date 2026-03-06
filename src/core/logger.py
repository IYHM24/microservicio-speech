import logging
import os

def get_logger(name: str):
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(level=log_level)
    return logging.getLogger(name)