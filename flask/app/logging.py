import logging
from logging.handlers import RotatingFileHandler
import time


def get_user_logger() -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
    formatter.converter = time.gmtime

    file_handler = RotatingFileHandler("./app/logs/user.log", maxBytes=2000000, backupCount=10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
