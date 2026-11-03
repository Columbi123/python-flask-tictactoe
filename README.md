# Крестики-нолики: Python + Flask API

Многослойное учебное веб-приложение с REST-подобным API для игры против компьютера. Ход компьютера выбирается алгоритмом Minimax. Для хранения игр используется потокобезопасное in-memory хранилище.

## Архитектура

- `src/web` — обработчики HTTP, модели запросов и ответов.
- `src/domain` — игровая логика и Minimax.
- `src/datasource` — in-memory репозиторий.
- `src/di` — создание зависимостей.

## Запуск (Python 3.10+)

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# Linux / macOS: source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
```

Запросы:

```bash
curl -X POST http://127.0.0.1:5000/game
# Подставьте полученный uuid и актуальное игровое поле:
curl -X POST http://127.0.0.1:5000/game/UUID -H 'Content-Type: application/json' -d '{"field": [[1,0,0],[0,0,0],[0,0,0]]}'
```

## Проверки

```bash
python -m unittest discover -s tests -v
```

Это лабораторное приложение, не production-сервис. Состояние хранится только в памяти процесса, без долговременной БД; для публичного развёртывания потребуются сервер WSGI, настройки безопасности и отдельное хранилище.
