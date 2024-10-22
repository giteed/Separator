#!/usr/bin/env python
# Путь: pySeparator/separator.py
# Описание: Скрипт для разбиения файлов на части определённого размера с возможностью кодирования данных (hex или base64) и сохранением этих частей в указанную папку.

import os
import base64
import hashlib
import time
import math
import rich_click as click
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

# Инициализация Rich для красивого вывода
console = Console(force_terminal=True, color_system="256")

def calculate_md5(file_path):
    """Вычисление контрольной суммы файла."""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def calculate_total_size(directory):
    """Подсчёт общего размера всех файлов в указанной директории."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def format_size(size_bytes):
    """Форматирует размер файла в человекочитаемый формат."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def calculate_increase_percentage(original_size, new_size):
    """Вычисляет процент увеличения размера частей по сравнению с оригинальным файлом."""
    increase = ((new_size - original_size) / original_size) * 100
    return round(increase, 2)

def split_file(input_file, output_dir, chunk_size, encoding):
    """
    Разбивает файл на части заданного размера и сохраняет в указанную папку.
    Также вычисляет контрольную сумму файла и размер частей.

    :param input_file: Путь к исходному файлу.
    :param output_dir: Папка для сохранения частей.
    :param chunk_size: Размер части в КБ.
    :param encoding: Метод кодирования частей файла ('hex', 'base64' или 'base85').
    """
    if not os.path.isfile(input_file):
        console.print(f"[red]Ошибка:[/red] Файл '{input_file}' не найден.")
        return

    # Создаем отдельную папку для частей в output/
    base_file_name = os.path.basename(input_file).rsplit('.', 1)[0]
    output_dir = os.path.join(output_dir, base_file_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Вычисляем контрольную сумму исходного файла
    file_md5 = calculate_md5(input_file)

    # Размер исходного файла
    file_size = os.path.getsize(input_file)
    chunk_size_bytes = chunk_size * 1024
    num_chunks = (file_size + chunk_size_bytes - 1) // chunk_size_bytes

    # Прогресс-бар с переносом строки
    with Progress() as progress:
        console.print(f"\nРазбиение файла: {input_file} на части...\n")  # Добавляем перенос строки
        task = progress.add_task(f"\n", total=num_chunks)
        start_time = time.time()

        try:
            with open(input_file, 'rb') as file:
                index = 1
                while True:
                    chunk = file.read(chunk_size_bytes)
                    if not chunk:
                        break

                    chunk_file_name = os.path.join(output_dir, f"{base_file_name}_part_{index}.txt")

                    if encoding == 'hex':
                        encoded_chunk = chunk.hex()
                    elif encoding == 'base64':
                        encoded_chunk = base64.b64encode(chunk).decode('utf-8')
                    elif encoding == 'base85':
                        encoded_chunk = base64.b85encode(chunk).decode('utf-8')
                    else:
                        console.print(f"[red]Ошибка:[/red] Некорректный тип кодирования '{encoding}'.")
                        return

                    with open(chunk_file_name, 'w') as chunk_file:
                        chunk_file.write(encoded_chunk)

                    index += 1
                    progress.update(task, advance=1)

            # Добавляем перенос строки перед выводом таблицы
            console.print("\n")

            # Сохраняем контрольную сумму в файл
            with open(os.path.join(output_dir, "checksum.md5"), 'w') as checksum_file:
                checksum_file.write(file_md5)

            # Подсчёт общего размера всех частей
            total_size_parts = calculate_total_size(output_dir)

            # Вычисление процента увеличения размера
            increase_percentage = calculate_increase_percentage(file_size, total_size_parts)

            end_time = time.time()

            # Отчетная таблица
            #table = Table(title="Результат разбиения файла")
            # Отчетная таблица с добавлением названия кодирования
            table = Table(title=f"Результат разбиения файла ({encoding})")  # Добавляем название алгоритма кодирования в заголовок

            table.add_column("Файл", justify="right", style="cyan", no_wrap=True)
            table.add_column("Значение", style="magenta")

            table.add_row("Имя файла", os.path.basename(input_file))
            table.add_row("Размер исходного файла", format_size(file_size))
            table.add_row("Число частей", str(index - 1))
            table.add_row("Общий размер частей", format_size(total_size_parts))
            table.add_row("Общий размер увеличился", f"на +{increase_percentage}% от оригинала")
            table.add_row("Контрольная сумма (MD5)", file_md5)
            table.add_row("Время выполнения", f"{end_time - start_time:.2f} секунд")

            console.print(table)

            # Сообщение о завершении
            console.print(f"\n[bold green]✔ Файл успешно разбит на {index - 1} частей.[/bold green]")
            console.print(f"[bold green]✔ Контрольная сумма сохранена.[/bold green]")

        except Exception as e:
            console.print(f"[red]Ошибка при обработке файла:[/red] {e}")

@click.command()
@click.option('--input', 'input', required=True, help='Путь к исходному файлу для разделения на части.')
@click.option('--output', 'output', required=True, help='Путь к папке для сохранения частей.')
@click.option('--chunk-size', type=int, default=100, help='Размер каждой части в КБ (по умолчанию 100 КБ).')
@click.option('--encoding', type=click.Choice(['hex', 'base64', 'base85'], case_sensitive=False), default='base85', help='Тип кодирования частей файла (hex, base64, base85). По умолчанию base85.')
def main(input, output, chunk_size, encoding):
    """
    **Разбивает файл на части и сохраняет их в указанную папку.**

    В конце сохраняется контрольная сумма исходного файла.

    Пример использования:
    ```
    python3 separator.py --input input/yourfile.mp4 --output output/ --chunk-size 200 --encoding base85
    ```
    """
    split_file(input, output, chunk_size, encoding)

if __name__ == '__main__':
    main()
