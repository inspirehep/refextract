FROM python:3.11.6-slim-bullseye AS refextract

ARG APP_HOME=/refextract
WORKDIR ${APP_HOME}

COPY refextract refextract/

RUN apt update && apt install poppler-utils libmagic1 -y
COPY poetry.lock pyproject.toml README.md ${APP_HOME}

RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false \
    && poetry install --only main

ENTRYPOINT ["/bin/bash" ]

FROM refextract AS refextract-tests

RUN poetry install --with dev
COPY tests tests/
RUN poetry install
