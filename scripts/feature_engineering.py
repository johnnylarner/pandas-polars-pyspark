import polars as pl

from ppp.polars import (
    add_features,
    calc_cash_journeys_per_pickup,
    calc_result_most_frequent_three_routes,
    update_payment_type_as_string_values,
)
from ppp.util import CONFIG_PATH, DATA_PATH, load_config, logging_setup


def rename_columns_as_lowercase(df: pl.DataFrame) -> pl.DataFrame:
    """Returns a polars DataFrame containing
    the df DataFrame with all columns
    renamed to be lowercase.
    """
    return df.rename({col: col.lower() for col in df.columns})


def main():
    config = load_config(CONFIG_PATH)
    logger = logging_setup(config)

    parquet_dir = DATA_PATH / "year=2011" / "yellow_tripdata_2011-01.parquet"

    df = pl.read_parquet(parquet_dir)
    zone_df = pl.read_csv(DATA_PATH / "taxi+_zone_lookup.csv")

    df = rename_columns_as_lowercase(df)
    zone_df = rename_columns_as_lowercase(zone_df)
    df = update_payment_type_as_string_values(df)

    logger.info("df schema: %s", df.schema)
    logger.info("df preview: %s", df.head(5))

    payments = df.get_column("payment_type")
    logger.info("Unique payments: %s", payments.unique())

    df = add_features(df, zone_df)
    logger.info("df schema after add_features: %s", df.schema)
    logger.info("df preview after add_features: %s", df.head(5))

    top_three_routes = calc_result_most_frequent_three_routes(df)
    logger.info("top_three_routes: %s", top_three_routes)

    cash_journeys = calc_cash_journeys_per_pickup(df)
    logger.info("cash_journeys: %s", cash_journeys)


if __name__ == "__main__":
    main()
