# prompt_toolkit_menu.py
import subprocess
import logging
import time
import os
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import checkboxlist_dialog, message_dialog
from prompt_toolkit.completion import PathCompleter, WordCompleter
from modules.progress_tracker import track_progress
from gpt_logger import setup_logger, log_start_process, log_end_process, log_file_info, log_success, log_error

# Создание директории для логов, если её нет
os.makedirs("logs", exist_ok=True)

# Настройка логирования
setup_logger()
logging.basicConfig(filename="logs/prompt_toolkit_menu.log", level=logging.DEBUG, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def clear_log(log_file):
    """Очищает указанный лог-файл перед началом новой задачи."""
    with open(log_file, 'w'):
        pass

def run_process(command, log_file):
    """Запускает внешний процесс с отслеживанием прогресса."""
    clear_log(log_file)
    logging.debug(f"Запущен процесс: {' '.join(command)}")

    # Запуск процесса
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Ожидание появления нового лог-файла
    wait_time = 2
    while not os.path.exists(log_file):
        logging.warning(f"Ожидание создания лог-файла: {log_file}")
        time.sleep(0.5)

    logging.debug(f"Лог-файл {log_file} найден, начинается отслеживание прогресса.")
    time.sleep(wait_time)
    
    track_progress(log_file)

    process.communicate()
    logging.debug("Процесс завершен.")

    # Чтение и вывод заключительных строк лога
    with open(log_file, 'r') as f:
        for line in f:
            if "разделение завершено" in line.lower() or "восстановление завершено" in line.lower():
                print(line.strip())

    clear_log(log_file)

def split_file():
    """Команда для разрезания файла с заданными параметрами."""
    print("\n*** Справка по навигации для выбора JSON файла ***")
    print("• Стрелки и [Tab] для для перемещения.")
    print("• Нажмите [/] для фиксации папки и отображения её содержимого.")
    print("• После выбора файла нажмите [Enter].\n")
    print("• Нажмите [Ctrl+C] для выхода в любой момент.\n")

    file_completer = PathCompleter()
    file_path = prompt("Введите путь к файлу для разрезания (используйте Tab): ", completer=file_completer, default="input/")
    chunk_size = prompt("Введите размер куска (в КБ, по умолчанию 200): ", default="200")
    encoding_completer = WordCompleter(['hex', 'base64', 'base85'], ignore_case=True)
    encoding = prompt("Выберите кодирование (hex, base64, base85): ", completer=encoding_completer, default="base64")

    logging.info(f"Запуск разрезания файла: {file_path}, кодирование: {encoding}, размер куска: {chunk_size}")
    log_file = "logs/separator-silence.log"

    command = ['python3', '-u', 'separator-silence.py', '--input', file_path, '--output', 'output/', '--chunk-size', chunk_size, '--encoding', encoding]
    run_process(command, log_file)

def merge_file():
    """Команда для восстановления файла из частей."""
    print("\n*** Справка по навигации для выбора JSON файла ***")
    print("• Стрелки и [Tab] для для перемещения.")
    print("• Нажмите [/] для фиксации папки и отображения её содержимого.")
    print("• После выбора файла нажмите [Enter].\n")
    print("• Нажмите [Ctrl+C] для выхода в любой момент.\n")

    file_completer = PathCompleter()
    metadata_path = prompt("Введите путь к файлу с метаданными (JSON): ", completer=file_completer, default="output/")
    
    output_completer = PathCompleter()
    output_dir = prompt("Введите путь для сохранения восстановленного файла: ", completer=output_completer, default="output_merged/")

    logging.info(f"Запуск восстановления файла: {metadata_path}")
    log_file = "logs/merge_parts-silence.log"
    
    command = ['python3', '-u', 'merge_parts-silence.py', '--metadata', metadata_path, '--output', output_dir]
    run_process(command, log_file)

def main_menu():
    """Главное меню программы."""
    logging.debug("Запуск главного меню")
    
    while True:
        choices = [
            ("Разбить файл на части", split_file),
            ("Восстановить файл из частей", merge_file),
            ("Выход", lambda: exit())
        ]

        selected_option = checkboxlist_dialog(
            title="pyChainLite Separator & Merger menu.",
            text=(
                "Выберите действие:\n"
                "\n*** Навигация в меню ***\n"
                "• [Tab] и стрелки для перемещения.\n"
                "• Нажмите [Enter] для выбора и подтвердите Ok.\n"
                "• Поддержка мыши доступна.\n"
                "   \nCoding method:  hex, base64, base85"
            ),
            values=[(str(i), option[0]) for i, option in enumerate(choices)]
        ).run()

        if selected_option:
            selected_option = int(selected_option[0])
            logging.debug(f"Выбрано действие: {choices[selected_option][0]}")
            choices[selected_option][1]()
            break

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем. Завершение...")
