import pytest

from utils import log_decorator_args


@log_decorator_args()
def func_division(int1: int, int2: int) -> float:
    return int1 / int2


class TestLogDecorators:

    def test_valid_log_decorator(self, capsys: pytest.CaptureFixture) -> None:
        """Тестирование на логирование правлиьно отработанной функции"""
        func_division(5, 2)
        result = capsys.readouterr()

        assert result.out == "func_division. Ok\n"

    def test_valid_log_decorator_error(self, capsys: pytest.CaptureFixture) -> None:
        """Тестирование на логирование ошибки функции"""
        func_division(7, 0)
        result = capsys.readouterr()

        assert result.out == "func_division. Error: division by zero, Input: (7, 0),{}\n"
