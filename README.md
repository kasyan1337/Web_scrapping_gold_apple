# Gold Apple Парфюмерия: Сбор данных о продуктах

## Описание проекта

Этот проект предназначен для сбора и обработки данных о продуктах из раздела "Парфюмерия" интернет-магазина Gold Apple. Используя веб-скрапинг, программа собирает информацию о товарах, включая ссылку на продукт, наименование, цену, рейтинг пользователей, описание, инструкцию по применению и страну-производителя. Полученные данные сохраняются в формате CSV.

## Структура проекта

```
├── README.md
├── data
│   ├── Goldapple_parfyumeriya.csv
│   ├── PART_1.csv
│   └── PART_2.csv
├── main.py
├── mock_data
├── requirements.txt
├── src
│   ├── CSVFileMerger.py
│   ├── __init__.py
│   ├── scrape_part_1.py
│   └── scrape_part_2.py
└── tests
    ├── __init__.py
    ├── test_CSVFileMerger.py
    ├── test_scrape_part_1.py
    └── test_scrape_part_2.py
```

### Описание основных файлов и каталогов

- **main.py**: Главный скрипт для запуска проекта. Он запускает процесс сбора данных, обрабатывает их и объединяет результаты в единый CSV файл.

- **src/**: Каталог с исходными файлами, содержащими логику веб-скрапинга и обработки данных.
  - **CSVFileMerger.py**: Скрипт для объединения CSV файлов с данными.
  - **scrape_part_1.py**: Скрипт для сбора основной информации о продуктах.
  - **scrape_part_2.py**: Скрипт для сбора детализированной информации о продуктах.

- **data/**: Каталог для хранения сгенерированных CSV файлов.
  - **PART_1.csv**: Файл, содержащий основную информацию о продуктах.
  - **PART_2.csv**: Файл с детализированной информацией о продуктах.
  - **Goldapple_parfyumeriya.csv**: Итоговый файл с объединёнными данными.

- **tests/**: Каталог с тестами для проверки работоспособности кода.
  - **test_CSVFileMerger.py**: Тесты для модуля CSVFileMerger.
  - **test_scrape_part_1.py**: Тесты для модуля scrape_part_1.
  - **test_scrape_part_2.py**: Тесты для модуля scrape_part_2.

- **requirements.txt**: Файл с зависимостями, необходимыми для работы проекта.

## Установка и запуск

### Шаг 1: Клонирование репозитория

Сначала клонируйте репозиторий на локальный компьютер:

```bash
git clone https://github.com/kasyan1337/Web_scrapping_gold_apple
```

### Шаг 2: Создание и активация виртуального окружения

Рекомендуется использовать виртуальное окружение для установки зависимостей:

```bash
python3 -m venv venv
source venv/bin/activate  # для macOS/Linux
venv\Scripts\activate  # для Windows
```

### Шаг 3: Установка зависимостей

Установите необходимые зависимости:

```bash
pip install -r requirements.txt
```

### Шаг 4: Запуск проекта

Для запуска процесса сбора данных используйте команду:

```bash
python main.py
```

Скрипт выполнит следующие действия:
1. Соберет основную информацию о продуктах и сохранит её в `data/PART_1.csv`.
2. Спросит у пользователя, хочет ли он продолжить сбор детализированной информации (Part 2).
3. Соберет детализированную информацию и сохранит её в `data/PART_2.csv`.
4. Объединит оба файла в `data/Goldapple_parfyumeriya.csv`.

## Тестирование

Для запуска тестов используйте следующую команду:

```bash
pytest tests/
```

Тесты проверяют основные функциональности кода, включая сбор и обработку данных.

## Результаты

Итоговый файл с объединенными данными можно найти по следующему пути:

[Скачать Goldapple_parfyumeriya.csv](./data/Goldapple_parfyumeriya.csv)
