ARG PLATFORM=linux/arm64
ARG DATA_SOURCE=local
FROM --platform=$PLATFORM python:3.10

RUN pip install poetry==1.6.1 && poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml poetry.lock ./
ENV POETRY_REQUESTS_TIMEOUT 300
RUN poetry install --only main --no-root --no-interaction && \
    poetry cache clear pypi --all


COPY ./src /app/src
RUN poetry install --only-root

COPY ./scripts /app/scripts
COPY /config /app/config

CMD ["python3", "/app/scripts/feature_engineering.py", $DATA_SOURCE]
