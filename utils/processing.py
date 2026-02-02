def filter_by_state(list_dict: list[dict[str, str]], state: str = "EXECUTED") -> list[dict[str, str]]:
    """
    Функция для фильтрации массива словарей по ключу 'state'
    :param list_dict: массив словарей для фильтрации
    :param state: данные фильтрации
    :return: фильтрованный список
    """
    result = [item for item in list_dict if item.get("state", "") == state]
    return result


def sort_by_date(list_dict: list[dict[str, str]], reverse: bool = True) -> list[dict[str, str]]:
    """
    Фукция сортировки массива словарей по ключу 'date'
    :param list_dict: массив для сортировки
    :param reverse: по возрастанию(False) или убыванию(True).
    :return: отсортированный список
    """
    result = sorted(list_dict, key=lambda x: x.get("date", "0"), reverse=reverse)
    return result
