ARG BUILD_PLATFORM
FROM --platform=$BUILD_PLATFORM python:3.10

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
COPY /data/year=2011/yellow_tripdata_2011-01.parquet /app/data/year=2011/yellow_tripdata_2011-01.parquet
COPY /data/taxi+_zone_lookup.csv /app/data/taxi+_zone_lookup.csv

CMD ["python3", "/app/scripts/feature_engineering.py"]
