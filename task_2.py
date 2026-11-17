import re
from typing import Callable, Iterator

# Дійсне число, відокремлене пробілами (або початком чи кінцем
# рядка) з обох боків. (?<!\S) і (?!\S) не дають захопити число,
# «приклеєне» до слова чи розділового знака: "324.00." або "$27.45".
NUMBER_PATTERN = re.compile(r"(?<!\S)\d+(?:\.\d+)?(?!\S)")


def generator_numbers(text: str) -> Iterator[float]:
    """Генератор, що по черзі повертає всі дійсні числа з тексту."""
    for match in NUMBER_PATTERN.finditer(text):
        yield float(match.group())


def sum_profit(text: str, func: Callable[[str], Iterator[float]]) -> float:
    """Рахує загальний дохід.

    Підсумовує всі числа, які генератор func знаходить у тексті.
    """
    # Суми грошові, тому округлюємо до копійок: це також прибирає
    # похибку float (0.1 + 0.2 = 0.30000000000000004)
    return round(sum(func(text)), 2)


if __name__ == "__main__":
    text = (
        "Загальний дохід працівника складається з декількох частин: "
        "1000.01 як основний дохід, доповнений додатковими надходженнями "
        "27.45 і 324.00 доларів."
    )
    total_income = sum_profit(text, generator_numbers)
    print(f"Загальний дохід: {total_income}")
