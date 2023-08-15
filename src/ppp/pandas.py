import pandas as pd
from pandas import DataFrame

from ppp.common import PaymentType, ROUTE_COLUMNS


def add_features(trip_df: DataFrame, zone_df: DataFrame) -> tuple[DataFrame, DataFrame]:
    """Returns a pandas DataFrame containing
    all the features derived from NYC
    Taxi dataset to answer all business questions.
    """
    trip_df = rename_columns_as_lowercase(trip_df)
    zone_df = rename_columns_as_lowercase(zone_df)
    trip_df = update_payment_type_as_string_values(trip_df)
    trip_df = add_borough_and_zone(trip_df, zone_df, "pulocationid")
    trip_df = add_borough_and_zone(trip_df, zone_df, "dolocationid")
    return trip_df, zone_df


def rename_columns_as_lowercase(df: DataFrame) -> DataFrame:
    """Returns a pandas DataFrame containing
    the df DataFrame with all columns
    renamed to be lowercase.
    """

    return df.rename(columns={col: col.lower() for col in df.columns})


def update_payment_type_as_string_values(trip_df: DataFrame) -> DataFrame:
    """Returns a pandas DataFrame containing
    the trip_df DataFrame with the payment_type
    column updated to be string values.
    """
    # TODO: replace is slow, could be replaced with map

    map_dict = {i.value: i.name for i in PaymentType}
    return trip_df.replace({"payment_type": map_dict})


def add_borough_and_zone(
    trip_df: DataFrame, zone_df: DataFrame, location_col: str
) -> DataFrame:
    """Returns a pandas DataFrame containing
    the trip_df DataFrame with the borough
    and zone columns added for `location_col`.

    The new columns will be prefixed with
    `location_col` and an underscore.
    """
    borough_zone_cols = ["borough", "zone"]
    location_col_zone_id = "locationid"
    zone_df_renamed = zone_df.rename(
        columns={l: f"{location_col}_{l}" for l in borough_zone_cols}
    )
    return trip_df.merge(
        zone_df_renamed, how="left", left_on=location_col, right_on=location_col_zone_id
    ).drop(columns=location_col_zone_id)


def calc_result_most_frequent_three_routes(trip_df: DataFrame) -> DataFrame:
    """Returns a pandas DataFrame containing
    most frequently routes including the
    number of times each route was travelled.
    """

    start_and_stop_of_trip_is_known = (trip_df.pulocationid_borough != "Unknown") & (
        trip_df.dolocationid_borough != "Unknown"
    )
    trips_with_known_start_stop = trip_df[start_and_stop_of_trip_is_known].filter(
        ROUTE_COLUMNS
    )
    trips_with_known_start_stop.shape

    trips_count = (
        trips_with_known_start_stop.groupby(ROUTE_COLUMNS)
        .size()
        .reset_index(name="num_trips")
        .sort_values("num_trips", ascending=False)
    )

    return trips_count.head(3)


def calc_cash_journeys_per_pickup(trip_df: DataFrame) -> DataFrame:
    """Returns a pandas DataFrame containing
    the number of cash journeys per pickup
    location.
    """

    is_cash_payment = trip_df["payment_type"] == "CASH"
    pickup_composite_key = ["pulocationid_borough", "pulocationid_zone"]

    trips_paid_cash_df = trip_df[is_cash_payment]

    return (
        trips_paid_cash_df[pickup_composite_key]
        .groupby(pickup_composite_key, as_index=False)
        .size()
        .rename(columns={"size": "num_cash_journeys"})
        .sort_values("num_cash_journeys", ascending=False)
    )


def calc_highest_tolls_per_route(trip_df: DataFrame) -> DataFrame:
    """Returns a pandas DataFrame containing
    the highest total tolls per route.
    """

    return (
        trip_df.groupby(ROUTE_COLUMNS)
        .agg(tolls_amount_sum=("tolls_amount", "sum"))
        .reset_index()
        .sort_values("tolls_amount_sum", ascending=False)
    )
