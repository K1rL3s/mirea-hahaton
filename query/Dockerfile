# Базовый образ Python
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Устанавливаем необходимые инструменты
RUN apt-get update && \
    apt-get install -y curl nmap && \
    apt-get clean

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.2 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --without dev

COPY ./app ./app
COPY ./query ./query
COPY ./database ./database
COPY ./di ./di
COPY ./utils ./utils

CMD ["python", "-m", "query"]
