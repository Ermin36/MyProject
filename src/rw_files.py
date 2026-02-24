import csv
from typing import Any, Dict, List

import numpy as np
import pandas as pd


class IOFiles:
    _path_file = ""
    _type = ""

    def __init__(self, file_path: str):
        """
        Инициализация класса
        :param file_path: путь к файлу
        """
        self._path_file = file_path
        self._type = file_path.split(".")[-1]

    def read(self) -> List[Dict[str, Any]]:
        """
        Чтения файла
        :return: список данных
        """
        if self._type == "csv":
            return self._read_csv()
        elif self._type == "xlsx":
            return self._read_xlsx()
        else:
            raise ValueError("Неизвестный тип файла")

    def set_path(self, new_path: str) -> None:
        """
        Изменение пути к файлу
        :param new_path: новый путь
        """
        self._path_file = new_path
        self._type = new_path.split(".")[-1]

    def _read_csv(self) -> list[dict[str, Any]]:
        """
        Внутренняя функция чтения csv файлов
        :return: список данных
        """
        data_list: list[dict[str, Any]] = []
        try:
            with open(self._path_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=";")

                # Читаем заголовки
                headers = next(reader)

                for row in reader:
                    # Создаем новый словарь для каждой строки
                    item: dict[str, Any] = {headers[i]: row[i] for i in range(len(row))}
                    data_list.append(item)

        except FileNotFoundError:
            raise FileNotFoundError("Файл не найден")

        return data_list

    def _read_xlsx(self) -> list[dict[str, Any]]:
        """
        Внутренняя функция чтения Excel файлов
        :return: список данных
        """
        df = pd.read_excel(self._path_file)
        columns = df.columns
        data_list: list[dict[str, Any]] = []

        for index in range(len(df)):
            item: dict[str, Any] = {}

            for column in columns:
                value = df[column][index]

                # Проверяем тип данных и обрабатываем NaN
                if isinstance(value, np.float64):
                    if not np.isnan(value):
                        item[column] = int(value)
                    else:
                        item[column] = None  # или другое значение по умолчанию
                else:
                    item[column] = value

            data_list.append(item)

        return data_list
