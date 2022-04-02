import logging
import time

def get_user_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    formatter.converter = time.gmtime
    file_handler = logging.FileHandler('./shadow/logs/user.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger