# ForceScan

# ПРОЕБАЛИ ЭТОМУ ГОВНИЩУ ВЫВОДЫ ДЕЛАЙТЕ САМИ https://github.com/SSSR-HACKATHON-2024/asp-24

## Сканирование портов и выявление уязвимостей

#### Специально для хакатона [Цифровой-Суверенитет.рф](https://xn----ctbbmaapfe8bebxhmwbjl2b.xn--p1ai/) от команды `git push --force`

## Запуск
1. Склонировать репозиторий и перейти в него:

    ```
    git clone https://github.com/rusandorx/hackathon.git git-push-force-frontend
    cd ./git-push-force-frontend
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
