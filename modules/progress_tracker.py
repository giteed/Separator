#  progress_tracker.py
import time
import re
from gpt_logger import log_error, log_success

def track_progress(log_file, total_parts=None):
    """
    Отслеживает прогресс выполнения разрезания или восстановления файлов на основе лог-файла.
    """
    part_pattern = re.compile(r"Часть (\d+)/(\d+) восстановлена|Часть (\d+) сохранена")
    total_parts_pattern = re.compile(r"Общее количество частей: (\d+)")
    log_pattern = re.compile(r'(?P<message>.+?)(?P<path>в: .+)$')  # Шаблон для финальных строк
    completed = False
    logged_parts = set()
    final_lines = []

    while not completed:
        try:
            with open(log_file, "r") as f:
                for line in f:
                    # Установка общего количества частей
                    if total_parts is None:
                        total_match = total_parts_pattern.search(line)
                        if total_match:
                            total_parts = int(total_match.group(1))
                            print(f"Общее количество частей установлено: {total_parts}")

                    # Отслеживание прогресса восстановления или разрезания
                    match = part_pattern.search(line)
                    if match:
                        part_number = int(match.group(1) or match.group(3))
                        logged_parts.add(part_number)
                        progress_percent = (len(logged_parts) / total_parts) * 100
                        print(f"\rПрогресс: {len(logged_parts)}/{total_parts} ({progress_percent:.2f}%) завершено", end="")

                    # Парсинг финальных строк для вывода сообщения и пути
                    log_match = log_pattern.search(line)
                    if log_match:
                        message = log_match.group('message').strip()
                        path = log_match.group('path').strip()
                        final_lines.append(f"Message: {message}\nPath: {path}")

                    # Проверка завершения задачи по фразам в логе
                    if "восстановление завершено" in line.lower() or "разделение завершено" in line.lower():
                        completed = True
                        #print("\n\nПроверка завершения задачи.")
                        log_success("Задача завершена успешно.")
                        break

            # Завершение при достижении 100%
            if total_parts and len(logged_parts) >= total_parts:
                completed = True
                print("\nЗадача завершена 100%")
                log_success("Задача завершена успешно.")
                break

            # Задержка для обновления
            time.sleep(0.3)

        except FileNotFoundError:
            log_error(f"Лог-файл {log_file} не найден.")
            time.sleep(0.5)

    # Вывод финальных строк
    if final_lines:
        print("\nФинальные сообщения:")
        for line in final_lines:
            print(line)
## 100% рабочий код 57754
