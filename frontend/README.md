# ForceScan

## Сканирование портов и выявление уязвимостей

#### Специально для хакатона [Цифровой-Суверенитет.рф](https://xn----ctbbmaapfe8bebxhmwbjl2b.xn--p1ai/) от команды `git push --force`

## Запуск
1. Склонировать репозиторий и перейти в него:

    ```
    git clone https://github.com/K1rL3s/mirea-hahaton-2024.git
    cd ./mirea-hahaton-2024/frontend
    ```

2. Создать и заполнить файл `.env` в корневой папке (пример: `.env.example`)
   ```
   VITE_API_BASE_URL=http://localhost:8000/api
   ```
3. Иметь установленный [Docker Engine](https://docs.docker.com/engine/)
4. Собрать и запустить:
    ```
    docker compose up -d --build
    ```
