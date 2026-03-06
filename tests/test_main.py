import pytest

from typing import Any

from src.main import get_user_input, processing_user_data, main
from src.main import quest_1, quest_2, quest_4, quest_5, quest_6, quest_break
from pytest_mock import MockerFixture


class TestFunctions:
    pass


class TestQuestFunction:
    data_input: dict[str, Any] = {
        "id_quest": 5,
        "user_data": 1,
        "out": [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "CANCELED"}, {"id": 3, "state": "PENDING"}],
        "user_input": {5: ["data"]},
    }

    def test_quest_break(self) -> None:
        """Тест функции заглушки для вопроса"""

        result = quest_break(**self.data_input)
        assert result[0]["id"] == 1

    @pytest.mark.parametrize(
        "user_input, path",
        [(1, "../data/operations.json"), (2, "../data/transactions.csv"), (3, "../data/transactions_excel.xlsx")],
    )
    def test_quest1(self, mocker: MockerFixture, user_input: int, path: str) -> None:
        """Тест функции обработки первого вопроса"""

        mock_read = mocker.patch("src.main.IOFiles.read")
        mock_set_path = mocker.patch("src.main.IOFiles.set_path")

        mock_read.return_value = [{"id": 1, "state": "test"}]
        mock_set_path.return_value = None
        self.data_input["user_data"] = user_input

        result = quest_1(**self.data_input)

        assert result == [{"id": 1, "state": "test"}]
        mock_set_path.assert_called_once_with(path)
        mock_read.assert_called_once()

    @pytest.mark.parametrize("user_input, state_type", [(1, "EXECUTED"), (2, "CANCELED"), (3, "PENDING")])
    def test_quest2(self, mocker: MockerFixture, user_input: int, state_type: str) -> None:
        """Тест функции обработки второго вопроса"""

        self.data_input["user_data"] = user_input

        mock = mocker.patch("src.main.filter_by_state")
        mock.return_value = [user_input]

        result = quest_2(**self.data_input)

        assert result == [user_input]
        mock.assert_called_once_with(self.data_input["out"], state_type)

    @pytest.mark.parametrize("user_input, type_out", [(1, False), (2, True)])
    def test_quest4(self, mocker: MockerFixture, user_input: int, type_out: bool) -> None:
        """Тест функции обработки четвёртого вопроса"""

        self.data_input["user_data"] = user_input

        mock_sort = mocker.patch("src.main.sort_by_date")
        mock_sort.return_value = [user_input]

        result = quest_4(**self.data_input)

        assert result[0] == user_input
        mock_sort.assert_called_once_with(self.data_input["out"], type_out)

    def test_quest5_input_1(self, mocker: MockerFixture) -> None:
        """Тест функции обработки пятого вопроса при входном ответе пользователя равному 1"""

        self.data_input["out"][:] = [1]

        mock_filter = mocker.patch("src.main.filter_by_currency")
        mock_filter.return_value = iter([3, 1, 2, 4])

        result = quest_5(**self.data_input)

        mock_filter.assert_called_once_with([3, 1, 2, 4], "RUB")
        assert result == [3, 1, 2, 4]

    def test_quest5_input_2(self, mocker: MockerFixture) -> None:
        """Тест функции обработки пятого вопроса при входном ответе пользователя равному 2"""

        self.data_input["user_data"] = 2
        out_data = [{"id": 5}]
        self.data_input["out"][:] = out_data

        mock_filter = mocker.patch("src.main.filter_by_currency")
        mock_filter.return_value = iter([3, 1, 2, 4])

        result = quest_5(**self.data_input)

        assert result == out_data
        mock_filter.assert_not_called()

    @pytest.mark.parametrize(
        "id_input, id_test, user_data, input_data, out_data, inf_run", [
            (1, 1, ['data'], ["test"], ["data"], True),
            (1, 2, ['data'], ['test'], ['test'], False),
            (3, 2, [], ['test'], ['test'], False)
        ]
    )
    def test_quest6_input_1(
        self, mocker: MockerFixture, id_input: int, id_test: int, user_data: list, input_data: list, out_data: list,
            inf_run: bool
    ) -> None:
        """Тест функции обработки шестого вопроса при входном ответе пользователя равному 1"""

        self.data_input['out'][:] = input_data
        self.data_input['user_input'][:] = {id_input:user_data}

        mock_filter = mocker.patch('src.main.process_bank_search')
        mock_filter.return_value = out_data

        result = quest_6(**self.data_input)

        assert result == out_data
        if inf_run:
            mock_filter.assert_called_once_with(user_data, user_data[0])

    def test_quest6_input_2(self, mocker: MockerFixture) -> None:
        """Тест функции обработки шестого вопроса при входном ответе пользователя равному 2"""

        self.data_input['out'][:] = [{'id':3}]
        self.data_input['user_data'] = 2

        mock_filter = mocker.patch('src.main.process_bank_search')
        mock_filter.return_value = [{"id":4}]

        result = quest_6(**self.data_input)

        assert result == [{'id':3}]
        mock_filter.assert_not_called()
