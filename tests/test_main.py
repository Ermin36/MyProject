from pydoc import resolve

import pytest

from src.main import get_user_input, processing_user_data, main
from src.main import quest_1, quest_2, quest_4, quest_5, quest_6, quest_break
from pytest_mock import MockerFixture

class TestFunctions:
    pass


class TestQuestFunction:
    def create(self):
        self.data_input = {
            "id_quest": 5,
            "user_data": 1,
            "out": [
                {"id": 1, 'state': "EXECUTED"},
                {'id': 2, 'state': "CANCELED"},
                {'id': 3, 'state': "PENDING"}
            ],
            "user_input": {5: "data"}
        }

    def test_quest_break(self) -> None:
        """Тест функции заглушки для вопроса"""
        self.create()
        result = quest_break(**self.data_input)
        assert result[0]["id"] == 1

    @pytest.mark.parametrize(
        "user_input, path", [
            (1, '../data/operations.json'),
            (2, '../data/transactions.csv'),
            (3, '../data/transactions_excel.xlsx')
        ]
    )
    def test_quest1(self, mocker: MockerFixture, user_input: int, path: str) -> None:
        """"""
        self.create()
        mock_read = mocker.patch('src.IOFiles.read')
        mock_set_path = mocker.patch('src.IOFiles.set_path')

        mock_read.return_value = [{'id': 1, "state": "test"}]
        mock_set_path.return_value = None
        self.data_input['user_data'] = user_input

        result = quest_1(**self.data_input)

        assert result == [{'id': 1, "state": "test"}]
        mock_set_path.assert_called_once_with(path)
        mock_read.assert_called_once()

    @pytest.mark.parametrize(
        "user_data, state_type", [
            (1, "EXECUTED"),
            (2, "CANCELED"),
            (3, "PENDING")
        ]
    )
    def test_quest2(self, mocker: MockerFixture, user_data: int, state_type: str) -> None:
        """"""
        self.create()
        self.data_input['user_data'] = user_data

        mock = mocker.patch('src.filter_by_state')
        mock.return_value = [{"id":0}]

        result = quest_2(**self.data_input)

        assert result[0]['state'] == state_type


    def test_quest4(self, mocker: MockerFixture) -> None:
        """"""
        self.create()
        self.data_input["user_data"] = 1

        mock_sort = mocker.patch('src.sort_by_date')
        mock_sort.return_value = [1]

        result = quest_4(**self.data_input)

        assert result[0] == 1
        pass