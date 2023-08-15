import pandas as pd
from pandas import DataFrame
from enum import Enum


# TODO: would be easier to use a dictionary directly
class PaymentType(Enum):
    """Enum representing the payment types
    for the NYC Taxi dataset.
    """

    CREDIT_CARD = 1
    CASH = 2
    NO_CHARGE = 3
    DISPUTE = 4
    UNKNOWN = 5
    VOIDED_TRIP = 6


# ROUTE_COLUMNS = [
#     "pulocationid_borough",
#     "pulocationid_zone",
#     "dolocationid_borough",
#     "dolocationid_zone",
# ]


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

    return trip_df.payment_type.replace(
        {i.value: i.name for i in PaymentType}
    ).to_frame()


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


def calc_result_most_frequent_three_routes(trip_df: DataFrame):
    __import__("IPython").embed()
