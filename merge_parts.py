#!/usr/bin/env python
# Путь: pySeparator/merge_parts.py
# Описание: Скрипт для восстановления оригинального файла из частей, сохранённых с помощью separator.py

import os
import base64
import rich_click as click
from rich.console import Console
from rich.table import Table

# Инициализация Rich для красивого вывода
console = Console(force_terminal=True, color_system="256")

def extract_part_number(filename):
    """Извлекает номер части из имени файла, чтобы отсортировать по номеру."""
    part = filename.split('_part_')[-1].split('.txt')[0]
    return int(part)

def merge_file(parts_dir, output_file, encoding):
    """
    Восстанавливает исходный файл из его частей и сохраняет в указанный файл.

    :param parts_dir: Папка, в которой хранятся части файла.
    :param output_file: Путь для сохранения восстановленного файла.
    :param encoding: Метод декодирования частей файла ('hex' или 'base64').
    """
    # Список всех частей файла с правильной сортировкой по номеру
    parts = sorted([f for f in os.listdir(parts_dir) if f.endswith('.txt') and '_part_' in f], key=extract_part_number)
    
    if not parts:
        console.print(f"[red]Ошибка:[/red] В папке '{parts_dir}' не найдены части файла.")
        return

    console.print(f"[green]Найдено {len(parts)} частей для восстановления в папке '{parts_dir}'[/green]")
    
    try:
        with open(output_file, 'wb') as output:
            for part in parts:
                part_file_path = os.path.join(parts_dir, part)
                with open(part_file_path, 'r') as part_file:
                    encoded_chunk = part_file.read()

                    # Декодируем части в зависимости от выбранной кодировки
                    if encoding == 'hex':
                        chunk = bytes.fromhex(encoded_chunk)
                    elif encoding == 'base64':
                        chunk = base64.b64decode(encoded_chunk)
                    else:
                        console.print(f"[red]Ошибка:[/red] Некорректный тип кодирования '{encoding}'.")
                        return

                    # Записываем декодированные данные в итоговый файл
                    output.write(chunk)
                    console.print(f"[cyan]Часть {part} добавлена к '{output_file}'[/cyan]")

        console.print(f"[bold green]Файл '{output_file}' успешно восстановлен из {len(parts)} частей.[/bold green]")
    
    except Exception as e:
        console.print(f"[red]Ошибка при восстановлении файла:[/red] {e}")

@click.command()
@click.option('--parts-dir', required=True, help='Путь к папке, содержащей части файла.')
@click.option('--output-file', required=True, help='Путь для сохранения восстановленного файла.')
@click.option('--encoding', type=click.Choice(['hex', 'base64'], case_sensitive=False), default='hex', help='Тип декодирования частей файла (hex или base64). По умолчанию hex.')
def main(parts_dir, output_file, encoding):
    """
    **Восстанавливает оригинальный файл из его частей и сохраняет в указанную папку.**

    ### Пример использования:
    1. Поместите все части файла в папку 'output_parts'.
    2. Для восстановления файла выполните следующую команду:

       `python3 merge_parts.py --parts-dir output_parts/ --output-file restored_file.avi --encoding base64`

    После этого восстановленный файл будет сохранён как 'restored_file.avi'.
    """
    # Выводим таблицу с параметрами
    table = Table(title="Параметры восстановления файла")
    table.add_column("Параметр", justify="right", style="cyan", no_wrap=True)
    table.add_column("Значение", style="magenta")

    table.add_row("Папка с частями", parts_dir)
    table.add_row("Итоговый файл", output_file)
    table.add_row("Кодирование", encoding)

    console.print(table)

    # Запуск основной функции для восстановления файла
    merge_file(parts_dir, output_file, encoding)

if __name__ == '__main__':
    main()
