from functools import wraps
from typing import Any, Callable


def log_decorator_args(filename: str | None = None) -> Callable:
    """
    Декоратор для логирования работы функции
    :param filename: путь к файлу, если нужно записать в файл, а не в консоль
    :return: декоратор
    """

    def log_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__}. Ok"
            except Exception as e:
                log_message = f"{func.__name__}. Error: {e}, Input: {args},{kwargs}"
                result = None

            if filename:
                with open(filename, "a") as file:
                    file.write(f"{log_message}\n")
            else:
                print(log_message)

            return result

        return wrapper

    return log_decorator


def json_decorator_from_operations(func: Callable) -> Callable:
    """
    Декоратор для преображения операций в csv и xlsx файлов в тип json
    :param func: функция для декорирования
    :return: декоратор
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        operations: list[dict] = func(*args, **kwargs)
        new_list: list[dict] = []

        def inf(item: dict, data: str) -> str:
            inf_data = str(item.get(data, "NONE"))
            if inf_data != "" and inf_data != "NONE" and inf_data != "nan":
                return inf_data
            else:
                return "NONE"

        for operation in operations:
            new_dict = {
                "id": operation.get("id", 0),
                "state": inf(operation, "state"),
                "date": inf(operation, "date"),
                "operationAmount": {
                    "amount": operation.get("amount", 0),
                    "currency": {"name": inf(operation, "currency_name"), "code": inf(operation, "currency_code")},
                },
                "description": inf(operation, "description"),
                "from": inf(operation, "from"),
                "to": inf(operation, "to"),
            }

            new_list.append(new_dict)

        return new_list

    return wrapper
