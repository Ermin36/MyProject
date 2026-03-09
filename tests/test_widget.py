import pytest

from src import get_date, mask_account_card

# functions


class TestMaskAccountCard:

    @pytest.mark.parametrize(
        "account_data, expect",
        [
            ("Счет 51235125151651681616", "Счет **1616"),
            ("Счет 35151561612435131305", "Счет **1305"),
            ("Visa 8465165141351313", "Visa 8465 16** **** 1313"),
            ("Master Card 4654651023331230", "Master Card 4654 65** **** 1230"),
        ],
    )
    def test_valid_mask_account_card(self, account_data: str, expect: str) -> None:
        """Тест маски на корректных данных счетов и карт"""
        result = mask_account_card(account_data)

        assert result == expect

    @pytest.mark.parametrize(
        "account_data, err_message",
        [
            ("Счет 8135131", "Длина номера должна быть 20 цифр"),
            ("Master Card 45363 25345", "Номер должен быть один"),
            ("Visa", "Номер не найден"),
            ("Счет 81335165151131551", "Длина номера должна быть 20 цифр"),
        ],
    )
    def test_invalid_mask_account_card(self, account_data: str, err_message: str) -> None:

        with pytest.raises(ValueError) as err:
            mask_account_card(account_data)

        assert str(err.value) == err_message


class TestDate:

    @pytest.mark.parametrize(
        "date, expect",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2015-07-23T11:15:05.431245", "23.07.2015"),
            ("2001-05-17T21:36:20.554235", "17.05.2001"),
            ("", ""),
        ],
    )
    def test_valid_date(self, date: str, expect: str) -> None:
        """Проверка даты при верных данных"""
        result = get_date(date)
        assert result == expect

    @pytest.mark.parametrize(
        "date, err_message",
        [
            ("2001.05.17T21:36:20.554235", "Не верный формат даты"),
            ("2024-03-11-02:26:18.671407", "Не верный формат даты"),
            ("2024--11T02:26:18.671407", "Нет данных даты"),
            ("--11T02:26:18.671407", "Нет данных даты"),
            ("2024-03-T02:26:18.671407", "Нет данных даты"),
        ],
    )
    def test_invalid_date(self, date: str, err_message: str) -> None:
        """Тест не правильных данных даты"""
        with pytest.raises(ValueError) as err:
            get_date(date)

        assert str(err.value) == err_message
