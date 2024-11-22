# Базовый образ Python
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Устанавливаем необходимые инструменты
RUN RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean

# Устанавливаем Poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.4.2 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --without dev

COPY ./app ./app
COPY ./database ./data
COPY ./di ./di
COPY ./utils ./utils

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "3"]
