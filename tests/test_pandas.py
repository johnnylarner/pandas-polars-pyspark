import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from ppp.pandas import (
    add_features,
    rename_columns_as_lowercase,
    update_payment_type_as_string_values,
    add_borough_and_zone,
    calc_result_most_frequent_three_routes,
    calc_cash_journeys_per_pickup,
    calc_highest_tolls_per_route,
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


def test_calc_result_most_frequent_three_routes(locations, top3_locations):
    trip_df = pd.DataFrame(locations)

    actual_df = calc_result_most_frequent_three_routes(trip_df)

    expected_df = pd.DataFrame(top3_locations)

    assert np.array_equal(actual_df.values, expected_df.values)


def test_calc_cash_journeys_per_pickup():
    trip_df = pd.DataFrame(
        {
            "payment_type": ["CASH", "CREDIT", "CASH", "NO_CHARGE", "CASH"],
            "pulocationid_borough": ["1", "2", "1", "3", "1"],
            "pulocationid_zone": ["1", "1", "1", "3", "4"],
        }
    )
    actual_df = calc_cash_journeys_per_pickup(trip_df)

    expected_df = pd.DataFrame(
        {
            "pulocationid_borough": ["1", "1"],
            "pulocationid_zone": ["1", "4"],
            "num_cash_journeys": [2, 1],
        }
    )

    assert_frame_equal(actual_df, expected_df)


def test_calc_highest_tolls_per_route(locations):
    locations_with_tolls = {
        **locations,
        "tolls_amount": [
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
            1.0,
        ],
    }

    trip_df = pd.DataFrame(locations_with_tolls)
    actual_df = calc_highest_tolls_per_route(trip_df)
    actual_df = actual_df[["tolls_amount_sum"]]

    expected_df = pd.DataFrame(
        {"tolls_amount_sum": [3.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0]}
    )

    assert np.array_equal(actual_df.values, expected_df.values)
