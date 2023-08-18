import importlib
import types

from ppp.util import CONFIG_PATH, DATA_PATH, load_config, logging_setup, get_rss


# def print_schema(df: module, module: types.ModuleType) -> None:
#     ...


# write a function that has a parameter that is a module


def main(module_name="polars"):
    # set up logger
    config = load_config(CONFIG_PATH)
    logger = logging_setup(config)
    module = importlib.import_module("ppp." + module_name)

    logger.info("resident memory before reading parquet [MB]: %s", get_rss())

    parquet_dir = DATA_PATH / "year=2011" / "yellow_tripdata_2011-01.parquet"

    df = module.read_parquet(parquet_dir)
    zone_df = module.read_csv(DATA_PATH / "taxi+_zone_lookup.csv")

    logger.info("df schema: %s", df.schema)
    logger.info("df preview: %s", df.head(5))
    logger.info("resident memory after reading parquet [MB]: %s", get_rss())

    df = module.add_features(df, zone_df)
    # logger.info("df schema after add_features: %s", df.schema)
    logger.info("df preview after add_features: %s", df.head(5))
    logger.info("resident memory after calling add_features [MB]: %s", get_rss())

    top_three_routes = module.calc_result_most_frequent_three_routes(df)
    logger.info("top_three_routes: %s", top_three_routes)

    cash_journeys = module.calc_cash_journeys_per_pickup(df)
    logger.info("cash_journeys: %s", cash_journeys)

    tolls_per_route = module.calc_highest_tolls_per_route(df)
    logger.info("tolls per route: %s", tolls_per_route)


if __name__ == "__main__":
    main()
