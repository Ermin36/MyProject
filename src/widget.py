from src import get_mask_account, get_mask_card_number

# functions


def mask_account_card(account_data: str) -> str:
    """
    Функция скрывает информацию об счёте или карте
    :param account_data: данные аккаунта
    :return: маска данных
    """
    data = account_data.split(" ")
    number_list = [item for item in data if item.isdigit()]
    word_list = [item for item in data if item.isalpha()]
    word = " ".join(word_list)

    if len(number_list) > 1:
        raise ValueError("Номер должен быть один")
    elif len(number_list) <= 0:
        raise ValueError("Номер не найден")

    if word_list[0] == "Счет":
        mask_account = get_mask_account(number_list[0])
    else:
        mask_account = get_mask_card_number(number_list[0])

    result = f"{word} {mask_account}"
    return result


def get_date(date: str) -> str:
    """
    Функция возвращает дату в формате 'ДД.ММ.ГГГГ'
    :param date данные даты
    :return: возвращает дату
    """
    if date == "":
        return ""

    if "-" not in date or "T" not in date:
        raise ValueError("Не верный формат даты")

    date_, time = date.split("T")
    year, month, day = date_.split("-")

    if not year or not month or not day:
        raise ValueError("Нет данных даты")

    date_format = "{0}.{1}.{2}"
    result = date_format.format(day, month, year)

    return result
