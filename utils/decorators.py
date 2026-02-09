from functools import wraps
from typing import Any, Callable


def log_decorator_args(filename: str | None = None) -> Callable:

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
