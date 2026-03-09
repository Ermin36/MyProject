from typing import Any, Generator

# functions


def filter_by_currency(
    transactions: list[dict[str, Any]], currency_code: str
) -> Generator[dict[str, Any], None, None]:
    """
    Фильтрация операций по типу валюты
    :param transactions: список
    :param currency_code: тип операции
    :return: отсортированные операции
    """
    for operation in transactions:
        currency = operation.get("operationAmount", {}).get("currency", {})

        code = currency.get("code", "")
        if code == currency_code:
            yield operation


def transaction_descriptions(transactions: list[dict[str, Any]]) -> Generator[str, None, None]:
    """
    Получение описания операций
    :param transactions: список операций
    :return: описание
    """
    for operation in transactions:
        description = operation.get("description", "None")
        yield description


def card_number_generator(num_start: int, num_end: int) -> Generator[str, None, None]:
    """
    Генерация номера карты
    :param num_start: начальное число
    :param num_end: конечное число
    :return: номер карты в формате XXXX XXXX XXXX XXXX
    """
    if num_start < 0 or num_end < 0:
        raise ValueError("Значение не может быть меньше нуля")

    if num_end > 10**16 - 1 or num_start > 10**16 - 1:
        raise ValueError("Значение не должно превышать 9999 9999 9999 9999")

    if num_start > num_end:
        raise ValueError("Начальное число не может быть больше конечного")

    for num in range(num_start, num_end):
        str_num = str(num)
        if len(str_num) < 16:
            str_num = "0" * (16 - len(str_num)) + str_num

        num_list = [str_num[:4], str_num[4:8], str_num[8:12], str_num[12:16]]
        result = " ".join(num_list)
        yield result
