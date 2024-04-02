import pathlib
import sys


def add_header_to_env(header: str):
    # Определение пути к файлу .env
    env_path = pathlib.Path(__file__).parent.parent / ".env"

    # Создание строки заголовка для комментария
    header_line = f" | {header.upper()} | "

    # Длина строки заголовка
    len_facets = 120

    # Формирование текста комментария
    comment = (
        f"# {"=" * len_facets}\n"
        + f"# | {header_line:-^{len_facets-4}} |\n"
        + f"# {"=" * len_facets}\n\n\n\n"
        + f"# {"=" * len_facets}\n\n\n"
    )

    # Открытие файла .env в режиме добавления текста
    with open(env_path, "a+") as f:
        f.write(comment)


if __name__ == "__main__":
    # Получение аргумента из командной строки
    header = sys.argv[1]

    # Добавление заголовка в файл .env
    add_header_to_env(header)
