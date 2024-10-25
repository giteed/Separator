
# pyChainLite Separator & Merger

## Оглавление
1. [Описание проекта](#описание-проекта)
2. [Основные функции](#основные-функции)
3. [Установка](#установка)
   - [Клонирование репозитория](#1-клонирование-репозитория)
   - [Создание и активация виртуального окружения](#2-создание-и-активация-виртуального-окружения)
   - [Установка зависимостей](#3-установка-зависимостей)
4. [Использование](#использование)
   - [Разбиение файла на части](#1-разбиение-файла-на-части)
   - [Восстановление файла из частей](#2-восстановление-файла-из-частей)
5. [Примеры использования](#примеры-использования)
6. [Сравнение методов кодирования](#сравнение-методов-кодирования)
7. [Зависимости](#зависимости)
8. [Лицензия](#лицензия)
9. [Дополнительные документы](#дополнительные-документы)

---

## Дополнительные документы

- [**Документация интерфейса меню prompt_toolkit**](docs/prompt_toolkit_menu.md): Интерфейс командной строки для удобного управления операциями разрезания и слияния файлов.

  Для работы с тихими скриптами, предназначенными для разрезания и восстановления файлов, вы можете ознакомиться с отдельными инструкциями:
  
- [**Документация по separator-silence.py**](docs/separator-silence.md): Скрипт для тихой разбивки файлов на части с сохранением метаданных.
- [**Документация по merge_parts-silence.py**](docs/merge_parts-silence.md): Скрипт для тихого восстановления файлов из частей на основе JSON-метаданных.


---

## Описание проекта

`pyChainLite Separator & Merger` — это набор Python-скриптов, предназначенных для разбиения файлов на части и последующего их восстановления. Скрипты поддерживают три метода кодирования — `hex`, `base64`, и `base85`, что делает их удобными для поблочной отправки файлов или хранения данных.

### Основные функции

- **Разбиение файлов**: Скрипт `separator.py` разбивает файл на несколько частей заданного размера, используя выбранное кодирование.
- **Восстановление файлов**: Скрипт `merge_parts.py` собирает части файла обратно в исходный файл, используя правильный порядок и выбранное кодирование.
- **Контрольные суммы**: В процессе разбивки и восстановления файлов вычисляется контрольная сумма (MD5) для проверки целостности данных.

---

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/giteed/separator.git
```

### 2. Создание и активация виртуального окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

Все зависимости указаны в файле `requirements.txt`. Установите их с помощью `pip`:

```bash
pip install -r requirements.txt
```

---

## Использование

### 1. Разбиение файла на части

Для разбиения файла на части используйте скрипт `separator.py`. Пример команды:

```bash
python3 separator.py --input 'input/yourfile.mp4' --output output/ --chunk-size 200 --encoding base64
```

#### Опции:
- `--input`: Путь к исходному файлу для разбиения.
- `--output`: Путь к папке, в которую будут сохранены части файла.
- `--chunk-size`: Размер каждой части в килобайтах (по умолчанию 100 КБ).
- `--encoding`: Кодирование для сохранения частей (`hex`, `base64`, `base85`). По умолчанию `base85`.

### 2. Восстановление файла из частей

Для восстановления файла используйте скрипт `merge_parts.py`. Пример команды:

```bash
python3 merge_parts.py --parts-dir output/ --output-file output_merged/restored_file.mp4 --encoding base85
```

#### Опции:
- `--parts-dir`: Путь к папке, где хранятся части файла.
- `--output-file`: Путь для сохранения восстановленного файла.
- `--encoding`: Кодирование, которое использовалось при разбиении (`hex`, `base64`, `base85`). По умолчанию `base85`.

---

## Примеры использования

### Разбиение файла

1. Поместите файл, который хотите разбить, в папку `input/`.
2. Выберите один из трёх вариантов кодирования:

```bash
# Кодирование hex (самое быстрое, но значительно увеличивает размер файлов)
python3 separator.py --input 'input/sample_file.mp4' --output output/ --chunk-size 200 --encoding hex

# Кодирование base64 (среднее по скорости и увеличению размера)
python3 separator.py --input 'input/sample_file.mp4' --output output/ --chunk-size 200 --encoding base64

# Кодирование base85 (самое компактное, но медленное)
python3 separator.py --input 'input/sample_file.mp4' --output output/ --chunk-size 200 --encoding base85
```

3. Части файла будут сохранены в папке `output/`.

### Восстановление файла

1. Убедитесь, что все части файла находятся в папке `output/`.
2. Используйте один из вариантов восстановления:

```bash
# Восстановление с использованием hex
python3 merge_parts.py --parts-dir output/sample_file --output-file output_merged/sample_file_restored.mp4 --encoding hex

# Восстановление с использованием base64
python3 merge_parts.py --parts-dir output/sample_file --output-file output_merged/sample_file_restored.mp4 --encoding base64

# Восстановление с использованием base85
python3 merge_parts.py --parts-dir output/sample_file --output-file output_merged/sample_file_restored.mp4 --encoding base85
```

3. Восстановленный файл будет сохранён в папке `output_merged/`.

---

## Сравнение методов кодирования

| Алгоритм  | Скорость    | Увеличение размера | Примечание                           |
|-----------|-------------|--------------------|--------------------------------------|
| `hex`     | Быстро      | +100%               | Подходит для быстрого разбиения, но увеличивает размер файлов в два раза. |
| `base64`  | Средняя     | +33%                | Хороший компромисс между скоростью и размером. Часто используется в интернет-протоколах. |
| `base85`  | Медленно    | +25%                | Самое компактное кодирование, но медленное. Подходит для экономии места.   |

### Примеры команд:

```bash
# Hex (быстрое, но сильно увеличивает размер)
python3 separator.py --input 'input/sample_file.mp4' --output output/ --chunk-size 200 --encoding hex

# Base64 (средняя скорость и размер)
python3 separator.py --input 'input/sample_file.mp4' --output output/ --chunk-size 200 --encoding base64

# Base85 (медленное, но компактное)
python3 separator.py --input 'input/sample_file.mp4' --output output/ --chunk-size 200 --encoding base85
```

---

### структура основных папок и список файлов:

```
pyChainLite/
│
├── input/                            # Папка для входных файлов, которые нужно разрезать
│   └── example_file.safetensors      # Пример входного файла
│
├── output/                           # Папка для хранения разрезанных частей и метаданных
│   └── parts/                        # Подпапка для частей файлов
│   └── json/                         # Подпапка для JSON-файлов с метаданными
│
├── output_merged/                    # Папка для хранения восстановленных файлов
│   └── restored_file.safetensors     # Пример восстановленного файла
│
├── logs/                             # Папка для логов работы программы
│   └── prompt_toolkit_menu.log       # Лог-файл для главного меню
│   └── separator-silence.log         # Лог-файл для разрезания
│   └── merge_parts-silence.log       # Лог-файл для восстановления
│
├── modules/                          # Папка с модулями программы
│   ├── progress_tracker.py           # Модуль для отслеживания прогресса операций
│   ├── gpt_logger.py                 # Модуль для логирования событий
│
├── prompt_toolkit_menu.py            # Главный скрипт для запуска меню
├── separator-silence.py              # Скрипт для разрезания файлов
├── merge_parts-silence.py            # Скрипт для восстановления файлов из частей
├── README.md                         # Файл с описанием проекта и инструкциями
└── prompt_toolkit_menu.md            # Документация для интерфейса меню `prompt_toolkit`
```

### Описание основных файлов

1. **`prompt_toolkit_menu.py`** — Основной интерфейс меню для управления разрезанием и восстановлением файлов.
2. **`separator-silence.py`** — Скрипт, отвечающий за разрезание файла на части.
3. **`merge_parts-silence.py`** — Скрипт для восстановления файла из частей.
4. **`modules/progress_tracker.py`** — Модуль отслеживания прогресса операций, выполняющихся в фоновом режиме.
5. **`modules/gpt_logger.py`** — Модуль для ведения логов всех событий в программе.
6. **`logs/`** — Папка, содержащая лог-файлы для каждой операции.
7. **`output/parts/` и `output/json/`** — Папки для хранения частей файлов и метаданных, соответственно.
8. **`output_merged/`** — Папка для сохранения файлов после восстановления.
   
## Зависимости

Проект использует следующие библиотеки:

- `rich`: Для цветного форматирования вывода в консоли.
- `click`: Для создания удобного интерфейса командной строки.
- `rich-click`: Для форматирования справки и вывода команд с цветным интерфейсом.

---

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности см. в файле `LICENSE`.

---



