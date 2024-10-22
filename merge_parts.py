#!/usr/bin/env python
# Путь: pySeparator/merge_parts.py
# Описание: Скрипт для восстановления оригинального файла из частей, сохранённых с помощью separator.py

import os
import base64
import hashlib
import time
import math  # Добавляем импорт библиотеки math
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

def format_size(size_bytes):
    """Форматирует размер файла в человекочитаемый формат."""
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB")
    i = int(math.floor(math.log(size_bytes, 1024)))  # Используем math для вычисления логарифма
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_name[i]}"

def merge_file(parts_dir, output_file, encoding):
    """
    Восстанавливает файл из частей и проверяет контрольную сумму.

    :param parts_dir: Папка, содержащая части файла.
    :param output_file: Путь для сохранения восстановленного файла.
    :param encoding: Метод декодирования частей файла ('hex', 'base64' или 'base85').
    """
    parts = sorted([f for f in os.listdir(parts_dir) if f.endswith('.txt') and '_part_' in f], key=lambda x: int(x.split('_part_')[-1].split('.')[0]))

    if not parts:
        console.print(f"[red]Ошибка:[/red] В папке '{parts_dir}' не найдено частей для восстановления.")
        return

    # Прогресс-бар с переносом строки
    with Progress() as progress:
        console.print(f"\nВосстановление файла: {output_file} из частей...\n")
        task = progress.add_task(f"\n", total=len(parts))  # Прогресс-бар без текста, перенос строки
        start_time = time.time()

        try:
            with open(output_file, 'wb') as output:
                for index, part in enumerate(parts, start=1):
                    part_path = os.path.join(parts_dir, part)

                    with open(part_path, 'r') as part_file:
                        encoded_data = part_file.read()

                        if encoding == 'hex':
                            decoded_data = bytes.fromhex(encoded_data)
                        elif encoding == 'base64':
                            decoded_data = base64.b64decode(encoded_data)
                        elif encoding == 'base85':
                            decoded_data = base64.b85decode(encoded_data)
                        else:
                            console.print(f"[red]Ошибка:[/red] Некорректный тип декодирования '{encoding}'.")
                            return

                        output.write(decoded_data)

                    progress.update(task, advance=1)

            # Подсчёт размера восстановленного файла
            restored_file_size = os.path.getsize(output_file)

            # Чтение контрольной суммы из файла
            checksum_file_path = os.path.join(parts_dir, "checksum.md5")
            restored_md5 = calculate_md5(output_file)

            if os.path.exists(checksum_file_path):
                with open(checksum_file_path, 'r') as checksum_file:
                    original_md5 = checksum_file.read().strip()

                # Проверка совпадения контрольных сумм
                end_time = time.time()
                console.print("\n")

                # Отчетная таблица
                table = Table(title=f"Результат восстановления файла ({encoding})")
                table.add_column("Параметр", justify="right", style="cyan", no_wrap=True)
                table.add_column("Значение", style="magenta")

                table.add_row("Имя файла", os.path.basename(output_file))
                table.add_row("Число частей", str(len(parts)))
                table.add_row("Размер восстановленного файла", format_size(restored_file_size))
                table.add_row("Контрольная сумма (MD5)", restored_md5)
                table.add_row("Время выполнения", f"{end_time - start_time:.2f} секунд")

                console.print(table)

                # Сообщение о завершении
                if restored_md5 == original_md5:
                    console.print(f"\n[bold green]✔ Файл успешно восстановлен. Контрольная сумма совпадает.[/bold green]")
                else:
                    console.print(f"\n[bold red]✘ Контрольная сумма не совпадает. Файл может быть поврежден.[/bold red]")

            else:
                console.print(f"[yellow]Предупреждение: файл с контрольной суммой не найден.[/yellow]")

        except Exception as e:
            console.print(f"[red]Ошибка при восстановлении файла:[/red] {e}")

@click.command()
@click.option('--parts-dir', required=True, help='Путь к папке, содержащей части файла.')
@click.option('--output-file', required=True, help='Путь для сохранения восстановленного файла.')
@click.option('--encoding', type=click.Choice(['hex', 'base64', 'base85'], case_sensitive=False), default='base85', help='Тип декодирования частей файла (hex, base64, base85). По умолчанию base85.')
def main(parts_dir, output_file, encoding):
    """
    **Восстанавливает файл из частей и сверяет контрольные суммы.**

    Пример использования:
    ```
    python3 merge_parts.py --parts-dir output/ --output-file restored_file.mp4 --encoding base85
    ```
    """
    merge_file(parts_dir, output_file, encoding)

if __name__ == '__main__':
    main()
