
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
7. [Структура проекта и описание файлов](#структура-проекта-и-описание-файлов)
8. [Зависимости](#зависимости)
9. [Лицензия](#лицензия)
10. [Связь с pyChainLite](#связь-с-pychainlite)

---

## Описание проекта

`pyChainLite Separator & Merger` — это набор Python-скриптов, предназначенных для разбиения файлов на части и их последующего восстановления. Он удобен для хранения, передачи и безопасного распределения больших данных.

### Основные функции

- **Разделение файлов** на части с использованием трех методов кодирования: `hex`, `base64` и `base85`, что делает данные совместимыми для различных систем хранения и передачи.
- **Восстановление файлов** из частей, используя встроенные JSON-метаданные.
- **Контроль целостности данных**: проверка с помощью контрольных сумм MD5 при разбиении и восстановлении файла.

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

Установите зависимости из файла `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Использование

### 1. Разбиение файла на части

Для разбиения файла на части выполните следующую команду:

```bash
python3 separator.py --input 'input/yourfile.mp4' --output output/ --chunk-size 200 --encoding base64
```

#### Опции
- `--input`: Путь к исходному файлу для разбиения.
- `--output`: Путь к папке для сохранения частей.
- `--chunk-size`: Размер каждой части в КБ (по умолчанию 100 КБ).
- `--encoding`: Кодировка для частей (`hex`, `base64`, `base85`). По умолчанию `base85`.

### 2. Восстановление файла из частей

Для восстановления файла из частей выполните:

```bash
python3 merge_parts.py --parts-dir output/ --output-file output_merged/restored_file.mp4 --encoding base85
```

#### Опции
- `--parts-dir`: Путь к папке с частями файла.
- `--output-file`: Путь для сохранения восстановленного файла.
- `--encoding`: Кодировка, использовавшаяся при разбиении (`hex`, `base64`, `base85`). По умолчанию `base85`.

---

## Примеры использования

### Разбиение файла

```bash
python3 separator.py --input 'input/sample_file.mp4' --output output/ --chunk-size 200 --encoding base64
```

### Восстановление файла

```bash
python3 merge_parts.py --parts-dir output/ --output-file output_merged/restored_file.mp4 --encoding base85
```

---

## Сравнение методов кодирования

| Алгоритм  | Скорость    | Увеличение размера | Примечание                                 |
|-----------|-------------|--------------------|--------------------------------------------|
| `hex`     | Быстро      | +100%             | Подходит для быстрого разбиения, но увеличивает размер файлов в два раза. |
| `base64`  | Средняя     | +33%              | Хороший компромисс между скоростью и размером. |
| `base85`  | Медленно    | +25%              | Компактное кодирование, но медленное.      |

---

## Структура проекта и описание файлов

```
separator/
│
├── input/                            # Папка для входных файлов для разрезания
│
├── output/                           # Папка для хранения частей и метаданных
│   ├── parts/                        # Части файлов
│   └── json/                         # JSON-файлы с метаданными
│
├── output_merged/                    # Папка для восстановления файлов
│
├── logs/                             # Логи программы
│
├── modules/                          # Модули программы
│   ├── progress_tracker.py           # Отслеживание прогресса
│   └── gpt_logger.py                 # Логирование
│
├── prompt_toolkit_menu.py            # Скрипт с интерфейсом меню
├── separator-silence.py              # Скрипт для разрезания
├── merge_parts-silence.py            # Скрипт для восстановления
└── README.md                         # Основное руководство
```

## Зависимости

- **rich** — Для красивого форматирования вывода в консоли.
- **click** — Удобные интерфейсы командной строки.
- **rich-click** — Поддержка цветного вывода командной строки.

---

## Лицензия

Этот проект распространяется под лицензией MIT.

---

## Связь с pyChainLite

`Separator` разрабатывался как самостоятельный инструмент для разрезания и восстановления файлов, но также интегрирован в проект [pyChainLite](https://github.com/giteed/pyChainLite) для выполнения операций с большими данными в блокчейне. 

`pyChainLite` использует `Separator` для разбиения данных на части и их распределенного хранения, что позволяет обеспечивать неизменяемость и защиту данных в рамках блокчейна.
