from typing import Callable


def return_zero_on_zero_division(
    function: Callable[..., float]
) -> Callable[..., float]:
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except ZeroDivisionError:
            return 0

    return wrapper


@return_zero_on_zero_division
def precision(true_positive: int, false_positive: int) -> float:
    return true_positive / (true_positive + false_positive)


@return_zero_on_zero_division
def recall(true_positive: int, false_negative: int) -> float:
    return true_positive / (true_positive + false_negative)
