# Force Scanner

## Сканирование портов и выявление уязвимостей

#### Специально для хакатона [Цифровой-Суверенитет.рф](https://xn----ctbbmaapfe8bebxhmwbjl2b.xn--p1ai/) от команды `git push --force`

## Запуск
1. Склонировать репозиторий и перейти в него:

    ```
    git clone https://github.com/K1rL3s/mirea-hahaton-2024.git
    cd ./mirea-hahaton-2024/backend
    ```

2. Создать и заполнить файл `.env` в корневой папке (пример: `.env.example`)
   ```
   NATS_URL=nats://nats:4222
   DB_URL=postgresql+psycopg://postgres:postgres@database:5432/postgres
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=postgres
   DELAY=1
   BACKEND_PORT=8000
   BACKEND_WORKERS=1
   QUERY_WORKERS=1
   ```
3. Иметь установленный [Docker Engine](https://docs.docker.com/engine/)
4. Собрать и запустить:
    ```
    docker compose up -d --build
    ```

## Реализованные фичи

- Перевод IP в домен и наоборот через tool.cy
- Сканирование:
  - Одного IP v4/v6
  - Диапазона IPv4
  - CIDR-нотации v4/v6
  - Произвольных IP v4/v6
- Гибкая настройка параметров nmap'а
- Получение последних сканирований
- Выбор локации (мокнуто, not worked)
- Генерация отчёта в PDF (на фронте)

## Из приятного

- Сваггер на `/api/docs` с возможностью потыкать бэк

## Формат данных

- Итоговый ответ бэка после скана:
   ```json
    {
      "task_id": "string",
      "end": true,
      "ips": [
        {
          "ip": "string",
          "ptr": "string",
          "end": true,
          "ports": {
            "open": [
              {
                "port": 0,
                "protocol": "string",
                "status": "string",
                "service": "string",
                "version": "string",
                "reason": "string",
                "vulnerabilities": [
                  {
                    "title": "string",
                    "description": "string",
                    "severity": "string"
                  }
                ]
              }
            ],
            "closed": [0]
          }
        }
      ]
    }
   ```

## Технологии

- `Python` как связующее
- `Postgres` как РСУБД для хранения отчётов сканов
- `Nats` как очередь для обмена сообщениями веб-сервера с запускателями nmap'а
- `FastAPI` как веб-сервер
- `FastStream` для работы с Nats'ом
- `SQLAlchemy` как ормка
- `dishka` как DI фреймворк
- `apscheduler` как планировщик
- `pandas` для обработки эксельки с уязвимостями
- `black` `isort` `ruff` `mypy` как контроль качества кода

## Структура

- `app` - веб-сервер
- `database` - модели бд и работа с ними
- `di` - DI провайдеры
- `migrations` - миграции бд
- `query` - очередь с запуском nmap'а
- `scheduler` - планировщик, обновляет эксель с уязвимостями
- `schemas` - схемы веб-API и очереди
- `services` - работа с сканами
- `static` - раздача отчётов nmap'а xml'ками
- `utils` - всячина =)

## Взаимодействие

![interaction.png](media/interaction.png)

![di-d2.png](media/di-d2.png)
