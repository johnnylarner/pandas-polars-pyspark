FROM python:3.10

WORKDIR /code

COPY pyproject.toml poetry.lock ./
COPY src ./src
COPY config ./config

RUN pip install poetry && poetry install --only main

COPY data/year=2011/yellow_tripdata_2011-01.parquet ./data/year=2011/yellow_tripdata_2011-01.parquet
COPY data/taxi+_zone_lookup.csv ./data/taxi+_zone_lookup.csv
COPY scripts/ ./scripts
RUN ls

CMD ["poetry", "run", "python3", "./scripts/feature_engineering.py"]
