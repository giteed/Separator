# gpt_logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_FILE = "gpt_push.log"

def setup_logger():
    """Настраивает логгер для записи только уникальных ключевых событий."""
    logger = logging.getLogger("GPTLogger")
    logger.setLevel(logging.INFO)

    handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024, backupCount=1)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    # Стираем лог при каждом запуске для избежания накопления данных
    open(LOG_FILE, 'w').close()

    logger.info("Логгер GPTLogger инициализирован и готов к записи.")
    return logger

# Инициализация логгера
logger = setup_logger()

def log_start_process(process_name):
    """Логирует начало процесса."""
    logger.info(f"Начало процесса: {process_name}")

def log_end_process(process_name):
    """Логирует завершение процесса."""
    logger.info(f"Завершен процесс: {process_name}")

def log_file_info(file_path):
    """Логирует информацию о файле, если он существует."""
    if os.path.exists(file_path):
        file_size = os.path.getsize(file_path)
        logger.info(f"Файл: {file_path} | Размер: {file_size} байт")
    else:
        log_error(f"Файл не найден: {file_path}")

def log_success(message):
    """Логирует успешное выполнение действия."""
    logger.info(f"Успешно: {message}")

def log_error(error_message):
    """Логирует уникальные ошибки только один раз."""
    if not hasattr(log_error, "logged_errors"):
        log_error.logged_errors = set()
        
    if error_message not in log_error.logged_errors:
        logger.error(error_message)
        log_error.logged_errors.add(error_message)

# Очистка зафиксированных ошибок при каждом запуске
log_error.logged_errors = set()
