# Сводка по городу

CLI-утилита: получает погоду (Open-Meteo) и курс валюты к рублю (Frankfurter), применяет простые правила и печатает сводку.

## Установка

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
python main.py --city Moscow
python main.py --city Moscow --currency EUR
python main.py --city Moscow --json
```

## Коды выхода

- 0: успех
- 2: ошибка аргументов
- 3: город или код валюты не найден
- 4: внешний сервис недоступен после повторов

## Тесты

```bash
python -m unittest discover tests
```