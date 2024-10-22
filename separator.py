#!/usr/bin/env python
# Путь: pySeparator/separator.py
# Описание: Скрипт для разбиения файлов на части определённого размера с возможностью кодирования данных (hex или base64) и сохранением этих частей в указанную папку.

import os
import base64
import rich_click as click
from rich.console import Console
from rich.table import Table

# Инициализация Rich для красивого вывода с принудительной активацией цвета
console = Console(force_terminal=True, color_system="256")

def split_file(input_file, output_dir, chunk_size, encoding):
    """
    Разбивает файл на части заданного размера и сохраняет в указанную папку.

    :param input_file: Путь к исходному файлу.
    :param output_dir: Папка для сохранения частей.
    :param chunk_size: Размер части в КБ.
    :param encoding: Метод кодирования частей файла ('hex' или 'base64').
    """
    # Проверяем, существует ли входной файл
    if not os.path.isfile(input_file):
        console.print(f"[red]Ошибка:[/red] Файл '{input_file}' не найден.")
        return

    # Проверяем, существует ли выходная папка
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Определяем имя файла без расширения для именования частей
    file_name = os.path.basename(input_file).rsplit('.', 1)[0]
    
    # Переводим размер части в байты
    chunk_size_bytes = chunk_size * 1024
    
    try:
        with open(input_file, 'rb') as file:
            index = 1
            while True:
                chunk = file.read(chunk_size_bytes)
                if not chunk:
                    break
                
                # Определяем имя для части файла
                chunk_file_name = os.path.join(output_dir, f"{file_name}_part_{index}.txt")
                
                # Кодирование данных в hex или base64
                if encoding == 'hex':
                    encoded_chunk = chunk.hex()
                elif encoding == 'base64':
                    encoded_chunk = base64.b64encode(chunk).decode('utf-8')
                else:
                    console.print(f"[red]Ошибка:[/red] Некорректный тип кодирования '{encoding}'.")
                    return
                
                # Сохраняем закодированные данные в файл
                with open(chunk_file_name, 'w') as chunk_file:
                    chunk_file.write(encoded_chunk)

                console.print(f"[green]Сохранена часть {index} как {chunk_file_name}[/green]")
                index += 1

        console.print(f"[bold]Файл успешно разбит на {index - 1} частей.[/bold]")
    
    except Exception as e:
        console.print(f"[red]Ошибка при обработке файла:[/red] {e}")

# Настройка rich-click для цветной справки
click.rich_click.MAX_WIDTH = 100  # Ограничение ширины справки
click.rich_click.USE_MARKDOWN = True  # Включение поддержки markdown в справке

@click.command()
@click.option('--input', required=True, help='Путь к исходному файлу для разделения на части.')
@click.option('--output', required=True, help='Путь к папке для сохранения частей.')
@click.option('--chunk-size', type=int, default=100, help='Размер каждой части в КБ (по умолчанию 100 КБ).')
@click.option('--encoding', type=click.Choice(['hex', 'base64'], case_sensitive=False), default='hex', help='Тип кодирования частей файла (hex или base64). По умолчанию hex.')
def main(input, output, chunk_size, encoding):
    """
    **Разбивает файл на части и сохраняет их в указанную папку.**

    ### Пример использования:
    1. Поместите файл, который хотите разбить, в папку 'input'.
    2. Для разбиения файла '12345.avi' на части по 200 КБ выполните следующую команду:

       `python3 separator.py --input input/12345.avi --output output/ --chunk-size 200 --encoding base64`

    После этого куски файла будут сохранены в папку 'output/'.
    """
    # Выводим таблицу с параметрами
    table = Table(title="Параметры выполнения")
    table.add_column("Параметр", justify="right", style="cyan", no_wrap=True)
    table.add_column("Значение", style="magenta")

    table.add_row("Входной файл", input)
    table.add_row("Папка для сохранения", output)
    table.add_row("Размер части (КБ)", str(chunk_size))
    table.add_row("Кодирование", encoding)

    console.print(table)

    # Запуск основной функции для разбиения файла
    split_file(input, output, chunk_size, encoding)

if __name__ == '__main__':
    main()
