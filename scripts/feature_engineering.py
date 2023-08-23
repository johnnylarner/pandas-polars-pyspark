from ppp.util import (
    CONFIG_PATH,
    DATA_PATH,
    load_config,
    logging_setup,
    get_rss,
    import_module,
)

from ppp.common import read_parquet_files, read_zone_lookup


def main():
    # set up logger
    config = load_config(CONFIG_PATH)
    logger = logging_setup(config)
    mod = import_module(config)

    logger.info("resident memory before reading parquet [MB]: %s", get_rss())

    zone_df = read_zone_lookup(config)
    df = read_parquet_files(config)

    logger.info("df schema: %s", df.schema)
    logger.info("df preview: %s", df.head(5))
    logger.info("resident memory after reading parquet [MB]: %s", get_rss())

    df = mod.add_features(df, zone_df)
    # logger.info("df schema after add_features: %s", df.schema)
    logger.info("df preview after add_features: %s", df.head(5))
    logger.info("resident memory after calling add_features [MB]: %s", get_rss())

    top_three_routes = mod.calc_result_most_frequent_three_routes(df)
    logger.info("top_three_routes: %s", top_three_routes)

    cash_journeys = mod.calc_cash_journeys_per_pickup(df)
    logger.info("cash_journeys: %s", cash_journeys)

    tolls_per_route = mod.calc_highest_tolls_per_route(df)
    logger.info("tolls per route: %s", tolls_per_route)


if __name__ == "__main__":
    main()
