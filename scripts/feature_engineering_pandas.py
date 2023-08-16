import os, psutil
import pandas as pd

from ppp.pandas import (
    add_features,
    calc_cash_journeys_per_pickup,
    calc_highest_tolls_per_route,
    calc_result_most_frequent_three_routes,
)
from ppp.util import CONFIG_PATH, DATA_PATH, load_config, logging_setup


def get_rss() -> float:
    psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)


def main():
    # set up logger
    config = load_config(CONFIG_PATH)
    logger = logging_setup(config)

    logger.info("resident memory before reading parquet [MB]: %s", get_rss())

    parquet_dir = DATA_PATH / "year=2011" / "yellow_tripdata_2011-01.parquet"

    df = pd.read_parquet(parquet_dir)
    zone_df = pd.read_csv(DATA_PATH / "taxi+_zone_lookup.csv")

    logger.info("df schema: %s", df.info())
    logger.info("df preview: %s", df.head(5))
    logger.info("resident memory after reading parquet [MB]: %s", get_rss())

    df, zone_df = add_features(df, zone_df)

    logger.info("df schema after add_features: %s", df.info())
    logger.info("df preview after add_features: %s", df.head(5))
    logger.info("resident memory after calling add_features [MB]: %s", get_rss())

    top_three_routes = calc_result_most_frequent_three_routes(df)
    logger.info("top_three_routes: %s", top_three_routes)

    cash_journeys = calc_cash_journeys_per_pickup(df)
    logger.info("cash_journeys: %s", cash_journeys)

    tolls_per_route = calc_highest_tolls_per_route(df)
    logger.info("tolls per route: %s", tolls_per_route)


if __name__ == "__main__":
    main()
