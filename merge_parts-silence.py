# merge_parts-silence.py
import os
import argparse
import json
import base64
import logging
import time

# Логирование
logging.basicConfig(filename="logs/merge_parts-silence.log", level=logging.INFO,  # Изменен уровень логирования на INFO
                    format="%(asctime)s - %(levelname)s - %(message)s")
logging.info("Программа запущена")

def merge_file(metadata_file, output_dir):
    """Функция для восстановления файла из частей."""
    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    # Проверка на наличие всех необходимых параметров
    required_keys = ['file_name', 'original_file_name', 'part_count', 'chunk_size', 'encoding', 'md5']
    missing_keys = [key for key in required_keys if key not in metadata]

    if missing_keys:
        logging.error(f"Недостаточно данных в метаданных. Требуемые параметры отсутствуют: {', '.join(missing_keys)}")
        return

    file_name = metadata['file_name']
    part_count = metadata['part_count']
    chunk_size = metadata['chunk_size']
    encoding = metadata['encoding']
    original_file_name = metadata['original_file_name']
    md5_hash = metadata['md5']

    # Директория, где находятся части
    parts_dir = os.path.join(os.path.dirname(metadata_file), '../parts')
    output_path = os.path.join(output_dir, original_file_name)

    logging.info(f"Начало восстановления файла в: {output_path}")

    with open(output_path, "wb") as output_file:
        for part_number in range(1, part_count + 1):
            part_file_name = f"{file_name[:5]}_{md5_hash[:5]}_part_{part_number:03d}.txt"
            part_file_path = os.path.join(parts_dir, part_file_name)

            if not os.path.isfile(part_file_path):
                logging.error(f"Часть файла не найдена: {part_file_path}")
                return

            with open(part_file_path, "rb") as part_file:
                part_data = part_file.read()

                if encoding == "hex":
                    output_file.write(bytes.fromhex(part_data.decode()))
                elif encoding == "base64":
                    output_file.write(base64.b64decode(part_data))
                elif encoding == "base85":
                    output_file.write(base64.b85decode(part_data))
                else:
                    logging.error(f"Неизвестная кодировка: {encoding}")
                    return
            # Убираем подробные DEBUG логи

    logging.info(f"Файл успешно восстановлен: {output_path}")

    # Создание нового файла метаданных для восстановленного файла
    restored_metadata = {
        "original_file_name": original_file_name,
        "restored_file_name": original_file_name,
        "restored_size": os.path.getsize(output_path),
        "restored_md5": md5_hash,
        "part_count": part_count,
        "chunk_size": chunk_size,
        "encoding": encoding,
        "restored_date": time.strftime('%Y-%m-%dT%H:%M:%S')
    }

    restored_metadata_path = os.path.join(output_dir, f"{md5_hash[:5]}_restored_{original_file_name}.json")
    with open(restored_metadata_path, "w") as metadata_out:
        json.dump(restored_metadata, metadata_out)

    logging.info(f"Метаданные восстановленного файла сохранены: {restored_metadata_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Восстановление файла из частей на основе метаданных")
    parser.add_argument('--metadata', required=True, help='Путь к JSON файлу с метаданными')
    parser.add_argument('--output', required=True, help='Путь для сохранения восстановленного файла')

    args = parser.parse_args()

    merge_file(args.metadata, args.output)
