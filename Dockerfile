FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get install -y curl nmap && \
    apt-get clean

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.8.2 POETRY_HOME=/root/poetry python3 -
ENV PATH="${PATH}:/root/poetry/bin"

WORKDIR /app

COPY pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --without dev

COPY ./app ./app
COPY ./query ./query
COPY ./scheduler ./scheduler
COPY ./database ./database
COPY ./di ./di
COPY ./migrations ./migrations
COPY ./alembic.ini ./alembic.ini
COPY ./schemas ./schemas
COPY ./utils ./utils
