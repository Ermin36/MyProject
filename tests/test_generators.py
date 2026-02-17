from typing import Any

import pytest

from src import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def transactions_list() -> list[dict[str, Any]]:

    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


class TestFilterByCurrency:

    def test_filter_by_currency_rub(self, transactions_list: list[dict[str, Any]]) -> None:
        """Фильтрация данных по RUB"""
        currency_filter = filter_by_currency(transactions_list, "RUB")
        assert next(currency_filter)["id"] == 873106923
        assert next(currency_filter)["id"] == 594226727

    def test_filter_in_empty_list(self, transactions_list: list[dict[str, Any]]) -> None:
        """Фильтрация пустого списка"""
        result = filter_by_currency([], "RUB")
        try:
            next(result)
            assert False
        except StopIteration:
            assert True

    def test_filter_by_currency_dst(self, transactions_list: list[dict[str, Any]]) -> None:
        """Фильтрация списка без соответствующей валютной операции"""
        result = filter_by_currency(transactions_list, "DST")

        try:
            next(result)
        except StopIteration:
            assert True


class TestTransactionDescriptions:

    def test_transaction_description(self, transactions_list: list[dict[str, Any]]) -> None:
        """Получение описания операции"""
        descriptions = transaction_descriptions(transactions_list)
        assert next(descriptions) == "Перевод организации"
        assert next(descriptions) == "Перевод со счета на счет"

    def test_transaction_description_in_empty_list(self) -> None:
        """Получение описания в пустом списке"""
        result = transaction_descriptions([])
        try:
            next(result)
            assert False
        except StopIteration:
            assert True


class TestCardNumberGenerator:

    @pytest.mark.parametrize(
        "num_min, num_max, expects",
        [
            (1, 7, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
            (127, 145, ["0000 0000 0000 0127", "0000 0000 0000 0128"]),
            (11147, 22256, ["0000 0000 0001 1147", "0000 0000 0001 1148"]),
        ],
    )
    def test_valid_card_number_generator(self, num_min: int, num_max: int, expects: list[str]) -> None:
        """Тест при верных значения"""
        result = card_number_generator(num_min, num_max)
        for expect in expects:
            assert next(result) == expect

    @pytest.mark.parametrize(
        "num_min, num_max, error_message",
        [
            (-4, 2, "Значение не может быть меньше нуля"),
            (7, 2, "Начальное число не может быть больше конечного"),
            (5, 10**16, "Значение не должно превышать 9999 9999 9999 9999"),
        ],
    )
    def test_invalid_card_number_generator(self, num_min: int, num_max: int, error_message: str) -> None:
        """Тест на корректность обработки ошибок и их сообщений"""
        with pytest.raises(ValueError) as err:
            result = card_number_generator(num_min, num_max)
            next(result)

        assert str(err.value) == error_message
