import json
from typing import Any

from .logger import create_logger

logger = create_logger(__name__, "utils.log")


def read_json(path: str) -> list[Any]:
    """
    Функция чтения JSON файла
    :param path: путь к файлу
    :return: список операций
    """
    logger.info("Старт функции read_json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                logger.error("Данные файла не являются списком")
                return []

            logger.info("Завершение функции")
            return data
    except FileNotFoundError:
        logger.error("Файл не найден")
        return []
