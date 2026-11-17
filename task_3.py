import sys
from collections import Counter

LOG_LEVELS = ("INFO", "DEBUG", "ERROR", "WARNING")


def parse_log_line(line: str) -> dict:
    """Розбирає рядок логу на дату, час, рівень і повідомлення.

    Формат рядка: "2024-01-22 08:30:01 INFO User logged in successfully."
    Якщо рядок не відповідає формату, кидає ValueError.
    """
    parts = line.strip().split(maxsplit=3)
    if len(parts) < 4:
        raise ValueError(f"неправильний формат рядка: {line.strip()!r}")

    date, time, level, message = parts
    level = level.upper()
    if level not in LOG_LEVELS:
        raise ValueError(f"невідомий рівень логування: {level!r}")

    return {"date": date, "time": time, "level": level, "message": message}


def load_logs(file_path: str) -> list:
    """Читає лог-файл і повертає список розібраних записів.

    Порожні рядки пропускаються, а рядки з неправильним форматом
    пропускаються з попередженням. Помилки відкриття файлу
    (FileNotFoundError, OSError) обробляє той, хто викликає функцію.
    """
    logs = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                logs.append(parse_log_line(line))
            except ValueError as error:
                print(f"Рядок {line_number} пропущено: {error}", file=sys.stderr)
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    """Повертає лише записи вказаного рівня логування."""
    level = level.upper()
    return list(filter(lambda log: log["level"] == level, logs))


def count_logs_by_level(logs: list) -> dict:
    """Рахує кількість записів для кожного рівня логування."""
    return dict(Counter(log["level"] for log in logs))


def display_log_counts(counts: dict) -> None:
    """Виводить таблицю «рівень логування — кількість»."""
    print(f"{'Рівень логування':<17}| Кількість")
    print(f"{'-' * 17}|{'-' * 10}")
    for level, count in counts.items():
        print(f"{level:<17}| {count}")


def display_log_details(logs: list, level: str) -> None:
    """Виводить усі записи вказаного рівня."""
    print(f"\nДеталі логів для рівня '{level.upper()}':")
    if not logs:
        print("Записів не знайдено.")
        return
    for log in logs:
        print(f"{log['date']} {log['time']} - {log['message']}")


def main() -> None:
    if len(sys.argv) not in (2, 3):
        print("Використання: python task_3.py <шлях до лог-файлу> [рівень]")
        sys.exit(1)

    file_path = sys.argv[1]
    level = sys.argv[2] if len(sys.argv) == 3 else None

    if level is not None and level.upper() not in LOG_LEVELS:
        print(
            f"Невідомий рівень логування: '{level}'. "
            f"Доступні рівні: {', '.join(LOG_LEVELS)}."
        )
        sys.exit(1)

    try:
        logs = load_logs(file_path)
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено.")
        sys.exit(1)
    except IsADirectoryError:
        print(f"'{file_path}' є директорією, а не файлом.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Файл '{file_path}' не є текстовим файлом у кодуванні UTF-8.")
        sys.exit(1)
    except OSError as error:
        print(f"Не вдалося прочитати файл '{file_path}': {error}")
        sys.exit(1)

    if not logs:
        print(f"У файлі '{file_path}' немає коректних записів логу.")
        sys.exit(1)

    display_log_counts(count_logs_by_level(logs))

    if level is not None:
        display_log_details(filter_logs_by_level(logs, level), level)


if __name__ == "__main__":
    main()
