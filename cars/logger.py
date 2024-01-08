import logging
import os
import re
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter('[%(asctime)s] %(levelname)s -> %(message)s')


def user_logger():
    logger = logging.getLogger('user_logger')
    if not logger.handlers:
        dir_path = Path("logs")
        dir_path.mkdir(exist_ok=True)

        log_file_path = dir_path / "user.log"

        user_file = TimedRotatingFileHandler(filename=log_file_path, when='midnight', interval=1, backupCount=31, encoding='utf-8')
        user_file.suffix = '%Y%m%d.log'
        user_file.setFormatter(formatter)
        logger.addHandler(user_file)
        logger.setLevel(logging.INFO)

    return logger

