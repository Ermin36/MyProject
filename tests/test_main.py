from typing import Any

import pytest
from pytest_mock import MockerFixture

from src.main import (get_user_input, main, processing_user_data, quest_1, quest_2, quest_4, quest_5, quest_6,
                      quest_break)


class TestFunctions:

    test_quest_data = [
        {
            "name": "test",
            "user_out": ["привет", "здравствуйте"],
            "out": ["Рад вас видеть!", "Мастер"],
            "id_out": [1, 3],
            "err": "Некорректный ввод: {status}",
        },
        {
            "name": "err_test",
            "user_out": ["test", "data"],
            "out": ["print1", "print2"],
            "id_out": [1, 3],
            "err": "Некорректный ввод: {status}",
        },
        {
            "name": "input_test",
            "user_out": ["get", "not"],
            "out": ["info", "skip"],
            "id_out": [1, 0],
            "input": "Ввод",
            "input_count": 1,
            "err": "Некорректный ввод: {status}",
        },
        {
            "name": "skip_test",
            "user_out": ["info", "skip"],
            "out": ["hello", "skip2"],
            "id_out": [1, 0],
            "goto": 1,
            "err": "Некорректный ввод: {status}",
        },
        {
            "name": "skip_quest",
            "user_out": ["det", "tek"],
            "out": ["hello", "hi"],
            "id_out": [1, 3],
            "err": "Некорректный ввод: {status}",
        },
    ]

    @pytest.mark.parametrize(
        "count1, count2, out_print, data_input, test_out, test_data",
        [
            (0, 1, ["test", "Рад вас видеть!"], ["привет"], [1], {}),
            (0, 0, [], [], [], {}),
            (
                0,
                2,
                ["test", "Мастер", "err_test", "Некорректный ввод: tek\n", "print1"],
                ["здравствуйте", "tek", "test"],
                [3, 1],
                {},
            ),
            (2, 3, ["input_test", "info", "Ввод"], ["get", "test"], [1], {0: ["test"]}),
            (3, 5, ["skip_test", "skip2"], ["skip"], [0, 0], {}),
        ],
    )
    def test_get_user_input(
        self,
        mocker: MockerFixture,
        count1: int,
        count2: int,
        out_print: list,
        data_input: list,
        test_out: list,
        test_data: dict,
    ) -> None:
        """Тест функции запроса ответов на вопросы от пользователя"""
        mock_read = mocker.patch("src.main.IOFiles.read")
        mock_read.return_value = self.test_quest_data[count1:count2]

        mock_input = mocker.patch("src.main.input")
        mock_input.side_effect = data_input

        mock_print = mocker.patch("src.main.print")

        result = get_user_input()

        for info in out_print:
            mock_print.assert_any_call(f"Программа: {info}")

        assert result == {"out": test_out, "user_input": test_data}

    def test_processing_user_data(self, mocker: MockerFixture) -> None:
        """Тестирование функции обработки ответов пользователя"""

        mock_func_map = mocker.patch(
            "src.main.func_map",
            new=[
                mocker.Mock(return_value=["Test1"]),
                mocker.Mock(return_value=["Test3"]),
                mocker.Mock(return_value=["Test4", "Test"]),
            ],
        )

        result = processing_user_data({"out": [1, 3, 4], "user_input": {}})

        assert result == ["Test4", "Test"]

        mock_func_map[0].assert_called_once_with(0, 1, [], {})
        mock_func_map[1].assert_called_once_with(1, 3, ["Test1"], {})
        mock_func_map[2].assert_called_once_with(2, 4, ["Test3"], {})

    def test_main_is_null(self, mocker: MockerFixture) -> None:
        """Тест пустого списка данных"""
        mocker.patch("src.main.get_user_input", return_value={})
        mocker.patch("src.main.processing_user_data", return_value=[])

        mock_print = mocker.patch("src.main.print")

        main()

        mock_print.assert_any_call(
            "Программа: Привет!\nДобро пожаловать в программу работы с банковскими транзакциями.\n"
        )
        mock_print.assert_any_call("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    def test_main_from_to(self, mocker: MockerFixture) -> None:
        """"""
        data_out = {
            "id": 435,
            "date": "2023-10-05T12:30:45.123456",
            "operationAmount": {"amount": 1000, "currency": {"name": "rub", "code": "RUB"}},
            "description": "Перевод средств",
            "from": "Карта 3151 3541 1253 9843",
            "to": "Счет 1231 1241 5432 1341 8365",
        }

        mocker.patch("src.main.get_user_input", return_value={})
        mocker.patch("src.main.processing_user_data", return_value=[data_out])
        mocker.patch("src.main.mask_account_card", side_effect=["Карта 3151 35** **** 9843", "Счет **8365"])
        mocker.patch("src.main.get_date", return_value="05.10.2023")
        mock_print = mocker.patch("src.main.print")

        main()

        mock_print.assert_any_call(
            "Программа: Привет!\nДобро пожаловать в программу работы с банковскими транзакциями.\n"
        )
        mock_print.assert_any_call("Программа:\nВсего банковских операций в выборке: 1\n")
        mock_print.assert_any_call(
            "05.10.2023 Перевод средств\nКарта 3151 35** **** 9843 -> Счет **8365\nСумма:1000 rub\n"
        )

    def test_main_to(self, mocker: MockerFixture) -> None:
        data_out = {
            "id": 435,
            "date": "2023-10-05T12:30:45.123456",
            "operationAmount": {"amount": 1000, "currency": {"name": "rub", "code": "RUB"}},
            "description": "Перевод средств",
            "to": "Счет 1231 1241 5432 1341 8365",
        }

        mocker.patch("src.main.get_user_input", return_value={})
        mocker.patch("src.main.processing_user_data", return_value=[data_out])
        mock_print = mocker.patch("src.main.print")
        mock_mask = mocker.patch("src.main.mask_account_card", return_value="Счет **8365")
        mock_get_date = mocker.patch("src.main.get_date", return_value="05.10.2023")

        main()

        mock_mask.assert_called_once_with("Счет 1231 1241 5432 1341 8365")
        mock_get_date.assert_called_once_with("2023-10-05T12:30:45.123456")

        mock_print.assert_any_call(
            "Программа: Привет!\nДобро пожаловать в программу работы с банковскими транзакциями.\n"
        )
        mock_print.assert_any_call("Программа:\nВсего банковских операций в выборке: 1\n")
        mock_print.assert_any_call("05.10.2023 Перевод средств\nСчет **8365\nСумма:1000 rub\n")


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
        self.data_input["user_data"] = 1

        mock_filter = mocker.patch("src.main.filter_by_currency")
        mock_filter.return_value = iter([3, 1, 2, 4])

        result = quest_5(**self.data_input)

        assert result == [3, 1, 2, 4]
        mock_filter.assert_called_once_with([3, 1, 2, 4], "RUB")

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
        "id_input, id_test, user_data, input_data, out_data, inf_run",
        [
            (1, 1, ["data"], ["test"], ["data"], True),
            (1, 2, ["data"], ["test"], ["test"], False),
            (3, 2, [], ["test"], ["test"], False),
        ],
    )
    def test_quest6_input_1(
        self,
        mocker: MockerFixture,
        id_input: int,
        id_test: int,
        user_data: list,
        input_data: list,
        out_data: list,
        inf_run: bool,
    ) -> None:
        """Тест функции обработки шестого вопроса при входном ответе пользователя равному 1"""
        self.data_input["id_quest"] = id_test
        self.data_input["out"] = input_data
        self.data_input["user_input"] = {id_input: user_data.copy()}
        self.data_input["user_data"] = 1

        mock_filter = mocker.patch("src.main.process_bank_search")
        mock_filter.return_value = out_data

        result = quest_6(**self.data_input)

        assert result == out_data
        if inf_run:
            text = user_data.pop()
            mock_filter.assert_called_once_with(input_data, text)
        else:
            mock_filter.assert_not_called()

    def test_quest6_input_2(self, mocker: MockerFixture) -> None:
        """Тест функции обработки шестого вопроса при входном ответе пользователя равному 2"""

        self.data_input["out"][:] = [{"id": 3}]
        self.data_input["user_data"] = 2

        mock_filter = mocker.patch("src.main.process_bank_search")
        mock_filter.return_value = [{"id": 4}]

        result = quest_6(**self.data_input)

        assert result == [{"id": 3}]
        mock_filter.assert_not_called()
