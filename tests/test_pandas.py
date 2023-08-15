import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from ppp.pandas import (
    add_features,
    rename_columns_as_lowercase,
    update_payment_type_as_string_values,
    add_borough_and_zone,
)


def test_rename_columns_as_lowercase():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    expected = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    result = rename_columns_as_lowercase(df)

    assert_frame_equal(result, expected)


def test_update_payment_type_as_string_values():
    df = pd.DataFrame({"payment_type": [6, 5, 4, 3, 2, 1]})

    expected_df = pd.DataFrame(
        {
            "payment_type": [
                "VOIDED_TRIP",
                "UNKNOWN",
                "DISPUTE",
                "NO_CHARGE",
                "CASH",
                "CREDIT_CARD",
            ]
        }
    )

    actual_df = update_payment_type_as_string_values(df)

    assert_frame_equal(actual_df, expected_df)


def test_add_borough_and_zone():
    trip_df = pd.DataFrame(
        {
            "pulocationid": [1, 2, 3, 4, 5],
            "dolocationid": [1, 2, 3, 4, 5],
        }
    )
    zone_df = pd.DataFrame(
        {
            "locationid": [1, 2, 3, 4, 5],
            "borough": ["Manhattan", "Queens", "Bronx", "Brooklyn", "Staten Island"],
            "zone": ["Midtown", "Astoria", "Riverdale", "Park Slope", "Tottenville"],
        }
    )

    actual_df = add_borough_and_zone(trip_df, zone_df, "pulocationid")
    expected_df = pd.DataFrame(
        {
            "pulocationid": [1, 2, 3, 4, 5],
            "dolocationid": [1, 2, 3, 4, 5],
            "pulocationid_borough": [
                "Manhattan",
                "Queens",
                "Bronx",
                "Brooklyn",
                "Staten Island",
            ],
            "pulocationid_zone": [
                "Midtown",
                "Astoria",
                "Riverdale",
                "Park Slope",
                "Tottenville",
            ],
        }
    )
    assert_frame_equal(actual_df, expected_df)
