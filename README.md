
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
7. [Интерфейс меню](#интерфейс-меню)
8. [Структура проекта и описание файлов](#структура-проекта-и-описание-файлов)
9. [Зависимости](#зависимости)
10. [Лицензия](#лицензия)
11. [Связь с pyChainLite](#связь-с-pychainlite)
12. [Дополнительные документы](#дополнительные-документы)

---

## Описание проекта

`pyChainLite Separator & Merger` — это набор Python-скриптов, предназначенных для разбиения файлов на части и их последующего восстановления. Инструмент подходит для хранения, передачи и безопасного распределения больших данных, а также интегрирован в блокчейн проект [pyChainLite](https://github.com/giteed/pyChainLite) для обеспечения распределенного хранения данных в сети.

### Основные функции

- **Разделение файлов** на части с использованием трех методов кодирования: `hex`, `base64`, `base85`, что делает данные совместимыми для различных систем хранения и передачи.
- **Восстановление файлов** из частей с использованием JSON-метаданных.
- **Контроль целостности данных**: проверка с помощью контрольных сумм MD5 при разбиении и восстановлении файла.

---

## Установка

### 1. Клонирование репозитория

Сначала склонируйте репозиторий:

```bash
git clone https://github.com/giteed/separator.git
```

Затем перейдите в папку проекта:

```bash
cd separator
```

### 2. Создание и активация виртуального окружения

Создайте виртуальное окружение **внутри папки проекта** для изоляции зависимостей:

```bash
python3 -m venv venv
```

Активируйте виртуальное окружение:

- **Linux/macOS**: 
  ```bash
  source venv/bin/activate
  ```
- **Windows**:
  ```powershell
  .\venv\Scripts\activate
  ```

### 3. Установка зависимостей

После активации виртуального окружения установите зависимости, указанные в `requirements.txt`:

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

## Интерфейс меню

### Описание меню

`Separator` включает удобный интерфейс командной строки на базе `prompt_toolkit`, который позволяет пользователям:

1. **Выбирать режим работы**:
   - Разделить файл на части.
   - Восстановить файл из частей.
   - Выход из программы.
  
2. **Устанавливать параметры для разбиения и слияния**: Пользователь может ввести путь к файлу, указать размер куска и выбрать кодирование.

3. **Просматривать прогресс операции**: Программа отображает ход выполнения задачи, количество обработанных частей, а также сохраняет логи в папке `logs/`.

### Скриншоты работы с меню

1. **Главное меню**

   - С помощью стрелок и клавиши `Enter` можно выбрать нужное действие: разрезать файл, восстановить или выйти.

2. **Консольное разрезание**

   - Пользователю предлагается ввести путь к файлу, выбрать размер куска и тип кодирования.
   - Программа отображает прогресс и сохраняет информацию о выполнении задачи в логах.

3. **Консольное слияние**

   - Пользователь вводит путь к JSON-файлу с метаданными и директорию для восстановления.
   - Отображается прогресс операции и информация о завершении.

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

Проект использует следующие библиотеки:

- **prompt_toolkit** — Для создания интерактивного меню.
- **rich** — Для красивого форматирования вывода в консоли.
- **click** — Удобные интерфейсы командной строки.
- **rich-click** — Поддержка цветного вывода командной строки.

---

## Лицензия

Этот проект распространяется под лицензией MIT.

---

## Связь с pyChainLite

`Separator` разрабатывался как самостоятельный инструмент для разрезания и восстановления файлов, но также интегрирован в проект [pyChainLite](https://github.com/giteed/pyChainLite) для выполнения операций с большими данными в блокчейне. `pyChainLite` использует `Separator` для разбиения данных на части и их распределенного хранения, что позволяет обеспечивать неизменяемость и защиту данных в рамках блокчейна.

---

## Дополнительные документы

- [**Документация интерфейса меню prompt_toolkit**](docs/prompt_toolkit_menu.md): Интерфейс командной строки для удобного управления операциями разрезания и слияния файлов.
- [**Документация по separator-silence.py**](docs/separator-silence.md): Скрипт для тихой разбивки файлов на части с сохранением мет

аданных.
- [**Документация по merge_parts-silence.py**](docs/merge_parts-silence.md): Скрипт для тихого восстановления файлов из частей на основе JSON-метаданных.

