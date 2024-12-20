# separator-silence.py
import os
import hashlib
import argparse
import json
import time
import base64
import logging

# Очищаем лог перед началом записи
with open("logs/separator-silence.log", "w") as f:
    f.write("")

# Настройка логирования
logging.basicConfig(filename="logs/separator-silence.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("===========separator-silence.py начал===========log %s==========", time.strftime('%Y-%m-%d %H:%M:%S'))

def split_file(input_file, output_dir, chunk_size_kb, encoding):
    """Функция для разрезания файла на части."""
    chunk_size = chunk_size_kb * 1024  # Размер куска в байтах
    file_name = os.path.basename(input_file)
    file_hash = hashlib.md5(file_name.encode()).hexdigest()[:5]

    # Директории для хранения частей и метаданных
    parts_dir = os.path.join(output_dir, f"{file_name[:5]}_{file_hash}", "parts")
    json_dir = os.path.join(output_dir, f"{file_name[:5]}_{file_hash}", "json")

    os.makedirs(parts_dir, exist_ok=True)
    os.makedirs(json_dir, exist_ok=True)

    start_time = time.time()

    # Подсчет общего количества частей
    file_size = os.path.getsize(input_file)
    total_parts = (file_size + chunk_size - 1) // chunk_size  # Общее количество частей
    logging.info(f"Общее количество частей: {total_parts}")

    with open(input_file, "rb") as f:
        part_number = 1
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            part_file_name = f"{file_name[:5]}_{file_hash}_part_{part_number:03d}.txt"
            part_file_path = os.path.join(parts_dir, part_file_name)

            with open(part_file_path, "wb") as part_file:
                if encoding == "hex":
                    part_file.write(chunk.hex().encode())
                elif encoding == "base64":
                    part_file.write(base64.b64encode(chunk))
                elif encoding == "base85":
                    part_file.write(base64.b85encode(chunk))
                else:
                    logging.error(f"Неизвестная кодировка: {encoding}")
                    return
            logging.info(f"Часть {part_number} сохранена")
            part_number += 1

    elapsed_time = time.time() - start_time

    # Создание JSON-файла с метаданными
    metadata = {
        "file_name": file_name,
        "original_file_name": file_name,
        "original_size": file_size,
        "part_count": part_number - 1,
        "chunk_size": chunk_size_kb,
        "encoding": encoding,
        "total_size": file_size,
        "md5": file_hash,
        "elapsed_time_seconds": elapsed_time,
        "creation_date": time.strftime('%Y-%m-%dT%H:%M:%S')
    }

    metadata_file = os.path.join(json_dir, f"{file_hash}_{file_name}.json")
    with open(metadata_file, "w") as metadata_out:
        json.dump(metadata, metadata_out)

    logging.info(f"Разделение завершено. Куски сохранены в: {parts_dir}")
    logging.info(f"JSON файл с метаданными сохранен в: {json_dir}/{file_hash}_{file_name}.json")
    logging.info("===========separator-silence.py завершен===========log %s==========", time.strftime('%Y-%m-%d %H:%M:%S'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Разрезание файла на части")
    parser.add_argument('--input', required=True, help='Путь к входному файлу')
    parser.add_argument('--output', required=True, help='Путь к директории для сохранения частей')
    parser.add_argument('--chunk-size', type=int, default=200, help='Размер куска в КБ')
    parser.add_argument('--encoding', choices=['hex', 'base64', 'base85'], default='base64', help='Кодирование для частей')

    args = parser.parse_args()

    split_file(args.input, args.output, args.chunk_size, args.encoding)
