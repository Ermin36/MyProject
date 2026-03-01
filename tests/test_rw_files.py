from unittest.mock import MagicMock, Mock, mock_open, patch
from src.rw_files import IOFiles
from typing import Any

import unittest
import numpy as np
import pandas as pd
import pytest




class TestReadJSONAndCSVAndXLSX(unittest.TestCase):

    def setUp(self) -> None:
        """Создание класса для тестов"""
        self.io_files = IOFiles("./data/transactions.csv")

    def test_valid_read_json(self) -> None:
        """Тест функции на верных данных"""

        self.io_files.set_path("./data/operations.json")
        json_data = self.io_files._read_json()

        assert isinstance(json_data, list)
        assert isinstance(json_data[0], dict)

    def test_invalid_read_json(self) -> None:
        """Тест функции при пустом пути или не верных данных в файле"""
        self.io_files.set_path("./data/test.json")
        result = self.io_files._read_json()
        assert result == []

    @patch("builtins.open", new_callable=mock_open)
    @patch("csv.reader")
    def test_read_valid_csv(self, mock: Mock, mock_file: MagicMock) -> None:
        """Тест функции чтения данных из csv файла"""
        mock.return_value = iter([["id", "name", "age"], ["1", "Иван", "25"], ["2", "Петр", "30"]])  # заголовки
        result = self.io_files._read_csv()
        expected = [
            {"id": "1", "name": "Иван", "age": "25"},
            {"id": "2", "name": "Петр", "age": "30"},
        ]
        assert result == expected
        mock.assert_called_once_with(mock_file(), delimiter=";")

    @patch("pandas.read_excel")
    def test_read_valid_xlsx(self, mock: Mock) -> None:
        """Тест функции чтения данных из excel файла"""
        mock_df = pd.DataFrame(
            {
                "id": [1.0, 2.0, np.nan],
                "name": ["Nikita", "Ivan", "Dima"],
            }
        )
        mock.return_value = mock_df

        io_file = IOFiles("./data/test.xlsx")
        result = io_file._read_xlsx()

        assert result == [{"id": 1, "name": "Nikita"}, {"id": 2, "name": "Ivan"}, {"id": None, "name": "Dima"}]
        mock.assert_called_once_with("./data/test.xlsx")

    def test_read_invalid_csv(self) -> None:
        """Проверка ошибки функции чтения csv файла, если файл не найден"""
        io_file = IOFiles("./test.csv")
        with pytest.raises(FileNotFoundError) as err:
            io_file.read()

        assert str(err.value) == "Файл не найден"


class TestClassIOFiles:
    def test_set_path(self) -> None:
        """Тестирование изменения пути к файлу"""
        io_files = IOFiles("./data/test.csv")
        io_files.set_path("./data/r.csv")
        assert io_files._path_file == "./data/r.csv"

    @patch.object(IOFiles, "_read_csv")
    def test_read_csv(self, mock_read: Mock) -> None:
        """Тест проверяет корректность работы метода read() для CSV файлов"""
        mock_read.return_value = [{"id": 1, "name": "Ivan"}]

        io_files = IOFiles("./data/test.csv")
        result = io_files.read()

        mock_read.assert_called_once()
        assert result == [{"id": 1, "name": "Ivan"}]

    @patch.object(IOFiles, "_read_xlsx")
    def test_read_xlsx(self, mock_read: Mock) -> None:
        """Тест проверяет корректность работы метода read() для Excel файлов"""
        mock_read.return_value = [{"id": 2, "name": "Nikita"}]

        io_files = IOFiles("./data/test.xlsx")
        result = io_files.read()

        mock_read.assert_called_once()
        assert result == [{"id": 2, "name": "Nikita"}]

    def test_read_invalid_file(self) -> None:
        """Тест проверяет корректность работы метода read() для неизвестного файла"""
        io_files = IOFiles("./data/test.txt")
        with pytest.raises(ValueError) as err:
            io_files.read()

        assert str(err.value) == "Неизвестный тип файла"
