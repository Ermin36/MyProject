import logging
from logging import Logger

LOGS_DIR = "./logs/"


def create_logger(name: str | None = None, file: str | None = None) -> Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if file is None:
        stream = logging.StreamHandler()
        logger.addHandler(stream)
    else:
        file_log = logging.FileHandler(LOGS_DIR + file, encoding="utf-8", mode="w")
        formated = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
        file_log.setFormatter(formated)

        logger.addHandler(file_log)

    return logger
