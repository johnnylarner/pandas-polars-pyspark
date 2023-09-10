import polars as pl
import pyarrow.parquet as pq
import s3fs
from polars import DataFrame

from ppp.common import ROUTE_COLUMNS, PaymentType


def _remove_s3_prefix_if_directory(path: str) -> str:
    """Removes the s3 prefix if the path is a directory."""
    if not path.startswith("s3://"):
        return path

    return path.lstrip("s3://")


def read_parquet(path: str) -> DataFrame:
    path = _remove_s3_prefix_if_directory(path)
    dataset = pq.ParquetDataset(path, filesystem=s3fs.S3FileSystem())
    return pl.from_arrow(dataset.read())


def add_features(trip_df: DataFrame, zone_df: DataFrame) -> DataFrame:
    """Returns a polars DataFrame containing
    all the features required for the NYC
    Taxi dataset.
    """
    trip_df = rename_columns_as_lowercase(trip_df)
    zone_df = rename_columns_as_lowercase(zone_df)
    trip_df = update_payment_type_as_string_values(trip_df)
    trip_df = add_borough_and_zone(trip_df, zone_df, "pulocationid")
    trip_df = add_borough_and_zone(trip_df, zone_df, "dolocationid")
    return trip_df


def rename_columns_as_lowercase(df: pl.DataFrame) -> pl.DataFrame:
    """Returns a polars DataFrame containing
    the df DataFrame with all columns
    renamed to be lowercase.
    """
    return df.rename({col: col.lower() for col in df.columns})


def update_payment_type_as_string_values(trip_df: DataFrame) -> DataFrame:
    """Returns a polars DataFrame containing
    the trip_df DataFrame with the payment_type
    column updated to be string values.
    """
    return trip_df.with_columns(
        pl.col("payment_type").map_dict({i.value: i.name for i in PaymentType})
    )


def add_borough_and_zone(
    trip_df: DataFrame, zone_df: DataFrame, location_col: str
) -> DataFrame:
    """Returns a polars DataFrame containing
    the trip_df DataFrame with the borough
    and zone columns added for `location_col`.

    The new columns will be prefixed with
    `location_col` and an underscore.
    """
    borough_zone_cols = ["borough", "zone"]
    zone_id_col = "locationid"

    id_borough_zone_df = zone_df.select([zone_id_col, *borough_zone_cols])
    id_borough_zone_df_with_suffix = id_borough_zone_df.rename(
        {col: f"{location_col}_{col}" for col in borough_zone_cols}
    )
    return trip_df.join(
        id_borough_zone_df_with_suffix,
        how="left",
        left_on=location_col,
        right_on=zone_id_col,
    )


def calc_result_most_frequent_three_routes(trip_df: DataFrame) -> DataFrame:
    """Returns a polars DataFrame containing
    most frequently routes including the
    number of times each route was travelled.
    """

    trip_start_and_stop_is_known = (pl.col("pulocationid_borough") != "Unknown") & (
        pl.col("dolocationid_borough") != "Unknown"
    )
    known_trips_df = trip_df.filter(trip_start_and_stop_is_known)

    num_trips_df = known_trips_df.groupby(ROUTE_COLUMNS).agg(
        pl.count().cast(pl.Int64).alias("num_trips")
    )

    return num_trips_df.top_k(3, by="num_trips")


def calc_cash_journeys_per_pickup(trip_df: DataFrame) -> DataFrame:
    """Returns a polars DataFrame containing
    the number of cash journeys per pickup
    location.
    """
    is_cash_payment = pl.col("payment_type") == PaymentType.CASH.name
    pickup_composite_key = ["pulocationid_borough", "pulocationid_zone"]

    cash_journeys_df = trip_df.filter(is_cash_payment)
    return (
        cash_journeys_df.groupby(*pickup_composite_key)
        .agg(pl.count().cast(pl.Int64).alias("num_cash_journeys"))
        .sort(by="num_cash_journeys", descending=True)
    )


def calc_highest_tolls_per_route(trip_df: DataFrame) -> DataFrame:
    """Returns a polars DataFrame containing
    the highest total tolls per route.
    """

    return (
        trip_df.groupby(ROUTE_COLUMNS)
        .agg(pl.col("tolls_amount").sum().suffix("_sum"))
        .sort(pl.col("tolls_amount_sum"), descending=True)
    )
