import pytest

from utils import get_mask_account, get_mask_card_number


class TestMaskCardNumber:

    @pytest.mark.parametrize(
        "card_number, expect",
        [
            (1315158342157982, "1315 15** **** 7982"),
            (5713546281342118, "5713 54** **** 2118"),
            (8431843522548135, "8431 84** **** 8135"),
        ],
    )
    def test_valid_mask_card(self, card_number: int, expect: str) -> None:
        """Проверка корректности маски номеров"""
        result = get_mask_card_number(card_number)

        assert result == expect

    @pytest.mark.parametrize(
        "card_number, err_message",
        [
            (515465, "Длина номера должна быть 16 цифр"),
            (-525245, "Номер не может быть отрицательным"),
            (51384255423158672, "Длина номера должна быть 16 цифр"),
        ],
    )
    def test_invalid_mask_card(self, card_number: int, err_message: str) -> None:
        """Проверка выброса ошибок при не правильном номере"""
        with pytest.raises(ValueError) as err:
            get_mask_card_number(card_number)

        assert str(err.value) == err_message


class TestMaskAccount:

    @pytest.mark.parametrize(
        "account_number, expect",
        [
            (1315158342157982, "**7982"),
            (5713546281342118, "**2118"),
            (8431843522548135, "**8135"),
        ],
    )
    def test_valid_mask_account(self, account_number: int, expect: str) -> None:

        result = get_mask_account(account_number)
        assert result == expect

    @pytest.mark.parametrize(
        "account_number, err_message",
        [
            (515465, "Длина номера должна быть 16 цифр"),
            (-525245, "Номер не может быть отрицательным"),
            (51384255423158672, "Длина номера должна быть 16 цифр"),
        ],
    )
    def test_invalid_mask_account(self, account_number: int, err_message: str) -> None:

        with pytest.raises(ValueError) as err:
            get_mask_account(account_number)

        assert str(err.value) == err_message
