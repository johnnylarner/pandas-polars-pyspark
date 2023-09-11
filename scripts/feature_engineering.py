import logging
import sys

import polars as pl

from ppp.polars import (
    add_features,
    calc_cash_journeys_per_pickup,
    calc_highest_tolls_per_route,
    calc_result_most_frequent_three_routes,
    read_parquet,
)
from ppp.util import (
    CONFIG_PATH,
    build_path_from_config,
    get_rss,
    load_config,
    logging_setup,
)

logger = logging.getLogger("ppp")


def main(data_flag: str = "local"):
    # set up logger
    config = load_config(CONFIG_PATH)
    logging_setup(config)

    logger.info("resident memory before reading parquet [MB]: %s", get_rss())

    data_config = config["data"]
    base_path = build_path_from_config(data_flag, data_config)

    trip_data = base_path / data_config["trip_file"]
    zone_data = base_path / data_config["zone_file"]

    logger.info("Reading trip data from %s", trip_data)
    df = read_parquet(str(trip_data))

    logger.info("Reading zone data from %s", zone_data)
    zone_df = pl.read_csv(str(zone_data))

    logger.info("df schema: %s", df.schema)
    logger.info("df preview: %s", df.head(5))
    logger.info("resident memory after reading parquet [MB]: %s", get_rss())

    df = add_features(df, zone_df)
    logger.info("df schema after add_features: %s", df.schema)
    logger.info("df preview after add_features: %s", df.head(5))
    logger.info("resident memory after calling add_features [MB]: %s", get_rss())

    top_three_routes = calc_result_most_frequent_three_routes(df)
    logger.info("top_three_routes: %s", top_three_routes)

    cash_journeys = calc_cash_journeys_per_pickup(df)
    logger.info("cash_journeys: %s", cash_journeys)

    tolls_per_route = calc_highest_tolls_per_route(df)
    logger.info("tolls per route: %s", tolls_per_route)


if __name__ == "__main__":
    data_flag_provided = len(sys.argv) > 1
    data_flag = sys.argv[1] if data_flag_provided else "local"

    if data_flag not in ("local", "s3"):
        raise ValueError(
            f"Invalid data flag {data_flag}. Valid values are 'local' and 's3'."
        )

    main(data_flag)
