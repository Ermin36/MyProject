import pytest

from src import filter_by_state, sort_by_date


# functions
@pytest.fixture
def list_for_test() -> list[dict[str, str]]:

    return [
        {"id": "434235", "count": "3"},
        {"state": "EXECUTED", "id": "15", "date": "15.03.24"},
        {"state": "Cancel", "id": "42", "date": "11.03.24"},
        {"state": "EXECUTED", "id": "15", "date": "05.03.24"},
        {"state": "NoN", "id": "15", "date": "16.03.24"},
        {"state": "EXECUTED", "id": "15", "date": "14.03.24"},
    ]


class TestFilterByState:

    def test_filter_by_executed(self, list_for_test: list[dict[str, str]]) -> None:
        """Тест фильтрации списка по стандартному значению"""
        result = filter_by_state(list_for_test)
        assert all(item["state"] == "EXECUTED" for item in result)
        assert len(result) == 3

    def test_filter_by_non(self, list_for_test: list[dict[str, str]]) -> None:
        """Фильтрация списка по выбранному значению"""
        result = filter_by_state(list_for_test, "NoN")
        assert len(result) == 1
        assert result[0]["state"] == "NoN"

    def test_filter_by_empty_list(self, list_for_test: list[dict[str, str]]) -> None:
        """Фильтрация пустого списка"""
        result = filter_by_state([])
        assert result == []


class TestSortByDate:

    def test_sort_by_date_desc(self, list_for_test: list[dict[str, str]]) -> None:
        """Сортировка по возростанию"""
        result = sort_by_date(list_for_test)
        dates = [item.get("date", "0") for item in result]

        assert dates == ["16.03.24", "15.03.24", "14.03.24", "11.03.24", "05.03.24", "0"]

    def test_sort_by_date_asc(self, list_for_test: list[dict[str, str]]) -> None:
        """Сортировка по убыванию"""
        result = sort_by_date(list_for_test, False)
        dates = [item.get("date", "0") for item in result]

        assert dates == ["16.03.24", "15.03.24", "14.03.24", "11.03.24", "05.03.24", "0"][::-1]
