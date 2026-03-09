from typing import Any

from src import (IOFiles, filter_by_currency, filter_by_state, get_date, mask_account_card, process_bank_search,
                 sort_by_date)


def get_user_input() -> dict[str, list]:
    """Функция сбора ответов пользователя на вопросы"""
    file = IOFiles("../data/system_quests.json")
    quests: list[dict] = file.read()

    out: dict = {"out": [], "user_input": {}}
    n_quest = 0
    for n, quest in enumerate(quests):
        if n_quest > 0:
            n_quest -= 1
            continue

        name: str = quest.get("name", "")
        user_out: list[str] = quest.get("user_out", [])
        ids: list[int] = quest.get("id_out", [])
        out_data: str = quest.get("out", "")
        inp_data: str = quest.get("input", "")
        input_count: int = quest.get("input_count", 0)
        data_err: str = quest.get("err", "")
        goto = quest.get("goto", 0)
        is_ok = False

        while not is_ok:
            print(f"Программа: {name}")
            user_input = input("Пользователь: ")

            for out_id, user_data in enumerate(user_out):
                if user_input.lower() == user_data.lower():
                    out["out"].append(ids[out_id])
                    if out_data != "":
                        print(f"Программа: {out_data[out_id]}")

                    if goto != 0 and ids[out_id] == 0:
                        out["out"].extend([0] * goto)
                        n_quest += goto

                    if inp_data != "" and ids[out_id] == 1 and input_count > 0:
                        out["user_input"][n] = []
                        list_data: list[str] = out["user_input"][n]
                        while input_count > 0:
                            print(f"Программа: {inp_data}")
                            input_user: str = input("Пользователь: ")

                            if input_user != "":
                                list_data.append(input_user)
                                input_count -= 1
                            else:
                                break

                    is_ok = True
                    print("\n")
                    break
            if not is_ok:
                err = data_err.format(status=user_input)
                print(f"Программа: {err}\n")

    return out


def quest_break(id_quest: int, user_data: int, out: list, user_input: dict) -> list:
    """Функция заглушка"""
    return out


def quest_1(id_quest: int, user_data: int, out: list, user_input: dict) -> list[Any]:
    """Функция обработки первого вопроса"""
    file = IOFiles("../data/none.txt")
    match user_data:
        case 1:
            file.set_path("../data/operations.json")
            out = file.read()
        case 2:
            file.set_path("../data/transactions.csv")
            out = file.read()
        case 3:
            file.set_path("../data/transactions_excel.xlsx")
            out = file.read()

    return out


def quest_2(id_quest: int, user_data: int, out: list, user_input: dict) -> list[Any]:
    """Функция обработки второго вопроса"""
    match user_data:
        case 1:
            out[:] = filter_by_state(out, "EXECUTED")
        case 2:
            out[:] = filter_by_state(out, "CANCELED")
        case 3:
            out[:] = filter_by_state(out, "PENDING")

    return out


def quest_4(id_quest: int, user_data: int, out: list, user_input: dict) -> list[Any]:
    """Функция обработки четвёртого вопроса"""
    match user_data:
        case 1:
            out[:] = sort_by_date(out, False)
        case 2:
            out[:] = sort_by_date(out, True)

    return out


def quest_5(id_quest: int, user_data: int, out: list, user_input: dict) -> list[Any]:
    """Функция обработки пятого вопроса"""
    match user_data:
        case 1:
            gen_currency = filter_by_currency(out, "RUB")
            out_list = []
            for operation in gen_currency:
                out_list.append(operation)
            out[:] = out_list
        case 2:
            return out

    return out


def quest_6(id_quest: int, user_data: int, out: list, user_input: dict) -> list[Any]:
    """Функция обработки шестого вопроса"""
    match user_data:
        case 1:
            user_data_inp: list[str] = user_input.get(id_quest, [])
            count: int = len(user_data_inp)
            if count != 0:
                text = user_data_inp.pop()
                out_list = process_bank_search(out, text)

                return out_list
            else:
                return out
        case 2:
            out = out

    return out


func_map = [quest_1, quest_2, quest_break, quest_4, quest_5, quest_6]


def processing_user_data(data: dict) -> list[Any]:
    """Функция обработки ответа пользователя"""
    user_input: list = data["out"]
    user_data_input: dict = data["user_input"]
    out: list = []
    for n, user_data in enumerate(user_input):
        if user_data != 0:
            out = func_map[n](n, user_data, out, user_data_input)

    return out


def main() -> None:
    """Главная функция программы"""
    print("Программа: Привет!\nДобро пожаловать в программу работы с банковскими транзакциями.\n")
    data = get_user_input()
    operations: list[dict] = processing_user_data(data)

    count = len(operations)
    if count > 0:
        print(f"Программа:\nВсего банковских операций в выборке: {count}\n")

    for operation in operations:
        date = ""
        if operation.get("date", "NONE") != "NONE":
            date = get_date(operation.get("date", ""))
        description = operation.get("description", "")

        data_from = operation.get("from", "NONE")
        card_from = ""
        if data_from != "NONE":
            card_from = mask_account_card(data_from)

        data_to = operation.get("to", "NONE")
        card_to = mask_account_card(data_to) if data_to != "NONE" else "null"

        amount = operation.get("operationAmount", {}).get("amount", 0)
        currency_name = operation.get("operationAmount", {}).get("currency", {}).get("name", "")

        data_format_from_to = f"{date} {description}\n{card_from} -> {card_to}\nСумма:{amount} {currency_name}\n"
        data_format_to = f"{date} {description}\n{card_to}\nСумма:{amount} {currency_name}\n"

        if data_from != "NONE":
            print(data_format_from_to)
        else:
            print(data_format_to)

    if len(operations) == 0:
        print("Программа: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")


if __name__ == "__main__":
    main()
