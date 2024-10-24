
# merge_parts-silence.py

## Описание

`merge_parts-silence.py` — это скрипт для тихой сборки (восстановления) исходного файла из нескольких частей на основе JSON-файла с метаданными. Скрипт работает в "тихом" режиме, не выводит информацию в консоль, а сохраняет все данные о процессе в лог-файл.

## Логика работы

1. **Чтение JSON метаданных** — скрипт принимает путь к JSON-файлу с метаданными, которые содержат информацию о частях и исходном файле.
2. **Проверка целостности частей** — на основе метаданных проверяется наличие всех необходимых частей.
3. **Восстановление файла** — части последовательно соединяются и создается исходный файл в указанной папке.
4. **Создание итогового JSON** — создается новый JSON-файл, в котором содержатся все данные о восстановленном файле, включая дату восстановления.
5. **Логирование** — информация о процессе восстановления записывается в лог-файл, включая ошибки и успешное завершение процесса.

## Пример запуска

```bash
python3 merge_parts-silence.py --metadata /path/to/metadata_file.json --output /path/to/output_dir
```

### Параметры:

- `--metadata` (обязательный) — Путь к JSON-файлу с метаданными о частях исходного файла.
  
  **Пример**: `/path/to/metadata_file.json`

- `--output` (обязательный) — Путь к директории, в которой будет сохранен восстановленный файл и итоговый JSON с метаданными.
  
  **Пример**: `/path/to/output_dir`

## Пример работы

### Входные данные:

- **JSON метаданные**: Файл `output/lift_v3.safetensors_<хэш>/json/lift_v3.safetensors_<хэш>.json`.
- **Части файла**: В директории `output/lift_v3.safetensors_<хэш>/parts`.

### Запуск:

```bash
python3 merge_parts-silence.py --metadata output/lift_v3.safetensors_<хэш>/json/lift_v3.safetensors_<хэш>.json --output output_merged/
```

### Логика работы:

1. Скрипт читает JSON-файл с метаданными, например: `output/lift_v3.safetensors_<хэш>/json/lift_v3.safetensors_<хэш>.json`.
2. Проверяет наличие всех частей файла в папке `output/lift_v3.safetensors_<хэш>/parts`.
3. Последовательно объединяет части в исходный файл, который сохраняется в директорию, указанную в параметре `--output`.
4. Восстановленный файл сохраняется в папку `output_merged/<имя файла>`, а рядом с ним создается новый JSON-файл с информацией о восстановлении.
5. Вся информация о ходе процесса записывается в лог.

### Пример JSON метаданных:

Пример файла метаданных, прочитанного скриптом:

```json
{
  "file_name": "lift_v3.safetensors",
  "original_file_name": "lift_v3.safetensors",
  "original_size": 151115808,
  "part_count": 738,
  "chunk_size": 200,
  "encoding": "base64",
  "total_size": 151142400,
  "md5": "441b385ddab60d0132e798116953430c",
  "elapsed_time_seconds": 5.42,
  "creation_date": "2024-10-24T13:17:53"
}
```

### Логика восстановления:

1. **Чтение метаданных**: Скрипт извлекает информацию из JSON-файла, чтобы определить путь к частям и параметры оригинального файла.
2. **Проверка целостности**: Проверяется наличие всех частей в папке `parts`.
3. **Соединение частей**: Все части объединяются в один файл с использованием заданного метода кодирования (например, `base64`).
4. **Сохранение результата**: Исходный файл сохраняется в указанную папку `output_merged/`.
5. **Запись итогового JSON**: Создается итоговый JSON-файл с информацией о восстановленном файле, включая дату восстановления.

### Итоговый JSON-файл:

```json
{
  "file_name": "lift_v3.safetensors",
  "original_file_name": "lift_v3.safetensors",
  "original_size": 151115808,
  "part_count": 738,
  "chunk_size": 200,
  "encoding": "base64",
  "total_size": 151142400,
  "md5": "441b385ddab60d0132e798116953430c",
  "elapsed_time_seconds": 5.42,
  "creation_date": "2024-10-24T13:17:53",
  "restored_date": "2024-10-24T14:05:23"
}
```

### Структура выходных данных:

После восстановления файла, структура выходных данных будет следующей:

```
output_merged/
│
└── lift_v3.safetensors
    └── lift_v3_restored_metadata.json
```

- Восстановленный файл (`lift_v3.safetensors`) будет помещен в указанную папку.
- Файл метаданных восстановления (`lift_v3_restored_metadata.json`) будет создан рядом с восстановленным файлом.

## Ошибки и логирование

- **Ошибки отсутствующих частей**: Если одна из частей отсутствует или не может быть найдена, процесс восстановления будет остановлен, а информация об этом запишется в лог.
- **Ошибки декодирования**: Если возникнет ошибка при декодировании части, она будет зафиксирована в лог.
- **Логи**: Все события записываются в лог-файл `logs/merge_parts-silence.log`.

Пример логов:

```plaintext
2024-10-24 13:18:32 - INFO - Запуск восстановления файла на основе метаданных: output/lift_v3.safetensors_<хэш>/json/lift_v3.safetensors_<хэш>.json
2024-10-24 13:18:32 - INFO - Восстановление файла завершено: output_merged/lift_v3.safetensors
2024-10-24 13:18:32 - INFO - Метаданные восстановления сохранены: output_merged/lift_v3_restored_metadata.json
```

## Дополнительная информация

- **Целостность данных**: Скрипт проверяет наличие всех частей перед восстановлением. Если части отсутствуют или повреждены, восстановление не будет завершено.
- **Логирование**: В процессе восстановления записываются только ошибки или завершенные этапы, чтобы снизить нагрузку на лог-файл.
- **Поддерживаемые кодировки**: Файл может быть восстановлен только с использованием тех же кодировок, которые были использованы для разрезания (например, `base64`, `hex`, `base85`).

