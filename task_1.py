from typing import Callable


def caching_fibonacci() -> Callable[[int], int]:
    """Повертає функцію fibonacci(n), яка кешує вже обчислені значення.

    Словник cache живе в області видимості caching_fibonacci, тому
    внутрішня функція «пам'ятає» його між викликами (замикання).
    """
    cache = {}

    def fibonacci(n: int) -> int:
        # Базові випадки рекурсії
        if n <= 0:
            return 0
        if n == 1:
            return 1

        # Значення вже обчислене: беремо його з кешу без рекурсії
        if n in cache:
            return cache[n]

        # Обчислюємо рекурсивно й зберігаємо результат у кеш
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci


if __name__ == "__main__":
    # Отримуємо функцію fibonacci
    fib = caching_fibonacci()

    # Використовуємо функцію fibonacci для обчислення чисел Фібоначчі
    print(fib(10))  # Виведе 55
    print(fib(15))  # Виведе 610
