import json

import polars as pl

from ppp.polars import add_features
from ppp.util import CONFIG_PATH, DATA_PATH, load_config, logging_setup


def main():
    config = load_config(CONFIG_PATH)
    logger = logging_setup(config)

    parquet_dir = DATA_PATH / "year=2009" / "yellow_tripdata_2009-01.parquet"

    df = pl.read_parquet(parquet_dir)
    logger.info("df schema: %s", df.schema)
    logger.info("df preview: %s", df.head(5))


if __name__ == "__main__":
    main()
