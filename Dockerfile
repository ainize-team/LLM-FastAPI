FROM python:3.8.13-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true

ENV PATH="$POETRY_HOME/bin:$VIRTUAL_ENVIRONMENT_PATH/bin:$PATH"

# Install Poetry
# https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    build-essential \
    curl \
    && curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python - \
    && apt-get purge --auto-remove -y \
    build-essential \
    curl

WORKDIR /app
COPY ./pyproject.toml ./pyproject.toml
COPY ./poetry.lock ./poetry.lock
RUN poetry install --no-dev

COPY ./llm_fastapi/ /app/

EXPOSE 8000

COPY ./start.sh /app/start.sh
RUN chmod +x /app/start.sh

CMD ./start.sh
