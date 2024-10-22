#!/bin/bash

# Путь: pySeparator/setup_and_help.sh
# Описание: Скрипт для создания виртуального окружения, установки зависимостей, подготовки папок проекта и вывода справки по использованию скрипта separator.py.

# Создание необходимых папок
echo "Создание папок input/ и output/..."
mkdir -p input output

# Проверка наличия separator.py
if [[ ! -f separator.py ]]; then
    echo "Ошибка: файл separator.py не найден. Убедитесь, что скрипт находится в текущей директории."
    exit 1
fi

# Создание виртуального окружения, если оно ещё не создано
if [[ ! -d venv ]]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
    echo "Виртуальное окружение создано."
fi

# Активация виртуального окружения
echo "Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей из requirements.txt, если файл существует
if [[ -f requirements.txt ]]; then
    echo "Установка зависимостей из requirements.txt..."
    pip install -r requirements.txt
else
    echo "Файл requirements.txt не найден, пропуск установки зависимостей."
fi

# Вывод справки по работе со скриптом separator.py
echo "Запуск справки по работе с separator.py..."
python3 separator.py --help

# Вывод примеров использования
echo ""
echo "Пример использования:"
echo "1. Поместите файл, который хотите разбить, в папку 'input'."
echo "2. Для разбиения файла '12345.avi' на части по 200 КБ выполните следующую команду:"
echo ""
echo "   python3 separator.py --input input/12345.avi --output output/ --chunk-size 200 --encoding base64"
echo ""
echo "После этого куски файла будут сохранены в папку 'output/'."
echo "Готово!"

# Оставляем виртуальное окружение активированным
$SHELL
