import pytest

from src.external_api import get_transaction_amount
from src import read_json
from unittest.mock import patch, Mock
from typing import Any


class TestGetTransactionAmount:

    def test_get_valid_transaction_amount_rub(self) -> None:
        """Проверка функции на рублях"""
        transactions = read_json("./data/operations.json")
        transaction_test = transactions[0]
        result = get_transaction_amount(transaction_test)

        assert result == 31957.58

    @patch("src.external_api.requests.get")
    def test_get_valid_transaction_amount_usd(self, mock_get: Mock) -> None:
        """Проверка функции на USD"""
        transactions = read_json("./data/operations.json")
        transaction_test = transactions[1]

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"result": "234.15"}

        result = get_transaction_amount(transaction_test, "15")

        api = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=8221.37&date=15"
        header = {"apikey": "jlcO10PXB2K44ChVW5W4ypaZ9mCwGr45"}

        assert result == 234.15
        mock_get.assert_called_once_with(api, headers=header)

    @pytest.mark.parametrize(
        "data, err_message",
        [
            ({"operationAmount": {"currency": {"name": "USD", "code": "USD"}}},
             "Не найдены данные amount"),
            ({"operationAmount": {"amount": "8221.37", "currency": {"code": "USD"}}},
            "Не найдены данные currency.name"),
            ({"operationAmount": {"amount": "8221.37", "currency": {"name": "USD"}}},
             "Не найдены данные currency.code"),
        ]
    )
    def test_get_invalid_transaction_amount_data(self, data: dict[str, Any], err_message: str) -> None:
        """Проверка функции на правильности обработки ошибок"""
        with pytest.raises(ValueError) as err:
            get_transaction_amount(data)

        assert str(err.value) == err_message

    @patch("src.external_api.requests.get")
    def test_get_invalid_transaction_amount_code(self, mock_get: Mock) -> None:
        """Проверка правильности данных при ошибке api"""
        transactions = read_json("./data/operations.json")
        transaction_test = transactions[1]

        mock_get.return_value.status_code = 201
        mock_get.return_value.json.return_value = {"result": "234.15"}

        result = get_transaction_amount(transaction_test)

        api = "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=8221.37"
        header = {"apikey": "jlcO10PXB2K44ChVW5W4ypaZ9mCwGr45"}

        assert result == 0.0
        mock_get.assert_called_once_with(api, headers=header)

