import re


def filter_by_state(list_dict: list[dict], state: str = "EXECUTED") -> list[dict]:
    """
    Функция для фильтрации массива словарей по ключу 'state'
    :param list_dict: массив словарей для фильтрации
    :param state: данные фильтрации
    :return: фильтрованный список
    """
    result = [item for item in list_dict if item.get("state", "").lower() == state.lower()]
    return result


def sort_by_date(list_dict: list[dict], reverse: bool = True) -> list[dict]:
    """
    Функция сортировки массива словарей по ключу 'date'
    :param list_dict: массив для сортировки
    :param reverse: по возрастанию(False) или убыванию(True).
    :return: Отсортированный список
    """
    result = sorted(list_dict, key=lambda x: x.get("date", "0"), reverse=reverse)
    return result


def process_bank_search(operations: list[dict], search: str) -> list[dict]:
    """
    Функция поиска по полю description
    :param operations: список операций
    :param search: искомые данные
    :return: список соответствующих операций
    """
    ret_list = []
    pattern = re.compile(search)

    for operation in operations:
        description = operation.get("description", "").lower()

        data = pattern.search(description)
        if data is not None:
            ret_list.append(operation)

    return ret_list


def process_bank_operations(operations: list[dict], categories: list) -> dict:
    """
    Функция сбора количества операций по категории
    :param operations: список операций
    :param categories: список категорий
    :return: словарь категорий типа dict[Any, int]
    """
    ret_dict = {}
    for category in categories:
        ret_dict[category] = 0

    for data in operations:
        description = data.get("description", "")
        for category in categories:
            if re.search(category,description) is not None:
                ret_dict[category] += 1
                continue

    return ret_dict
