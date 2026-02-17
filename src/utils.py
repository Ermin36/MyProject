import json
from typing import Any


def read_json(path: str) -> list[Any]:
    """
    Функция чтения JSON файла
    :param path: путь к файлу
    :return: список операций
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                return []

            return data
    except FileNotFoundError:
        return []
