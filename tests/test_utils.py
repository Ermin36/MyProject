from typing import Any

import pytest

from src import read_json


class TestReadJSONFile:

    def test_valid_read_json(self) -> None:
        """Тест функции на верных данных"""

        path = "../data/operations.json"
        json_data = read_json(path)

        assert isinstance(json_data, list)
        assert isinstance(json_data[0], dict)

    @pytest.mark.parametrize("path, data", [("./data/operations.json", []), ("../data/test.json", [])])
    def test_invalid_read_json(self, path: str, data: Any) -> None:
        """Тест функции при пустом пути или не верных данных в файле"""

        result = read_json(path)
        assert result == data
