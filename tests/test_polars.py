import polars as pl
import pytest
from polars.testing import assert_frame_equal

from ppp.polars import (
    add_borough_and_zone,
    calc_cash_journeys_per_pickup,
    calc_highest_tolls_per_route,
    calc_result_most_frequent_three_routes,
    update_payment_type_as_string_values,
)


@pytest.fixture
def locations():
    return {
        "pulocationid_borough": [
            "Manhattan",
            "Manhattan",
            "Manhattan",
            "Queens",
            "Queens",
            "Bronx",
            "Bronx",
            "Brooklyn",
            "Brooklyn",
            "Brooklyn",
            "Unknown",
            "Unknown",
            "Unknown",
        ],
        "pulocationid_zone": [
            "Upper East Side",
            "Upper East Side",
            "Upper East Side",
            "Astoria",
            "Hunters Point",
            "Riverdale",
            "Riverdale",
            "Williamsburg",
            "Williamsburg",
            "Bushwick",
            "Unknown",
            "Unknown",
            "Unknown",
        ],
        "dolocationid_borough": [
            "Queens",
            "Queens",
            "Queens",
            "Manhattan",
            "Manhattan",
            "Bronx",
            "Bronx",
            "Bronx",
            "Bronx",
            "Bronx",
            "Unknown",
            "Unknown",
            "Unknown",
        ],
        "dolocationid_zone": [
            "Astoria",
            "Astoria",
            "Astoria",
            "Upper East Side",
            "Lower East Side",
            "Fordham",
            "Fordham",
            "Riverdale",
            "Riverdale",
            "Riverdale",
            "Unknown",
            "Unknown",
            "Unknown",
        ],
    }


def assert_pl_frame_equal(
    actual_df, expected_df, check_row_order=False, **kwargs
) -> None:
    try:
        assert_frame_equal(
            actual_df, expected_df, check_row_order=check_row_order, **kwargs
        )
        assert True
        return
    except AssertionError as e:
        print(
            f"DataFrames are not equal. Expected:\n{expected_df},\nactual:\n{actual_df}"
        )
        raise e


def test_update_payment_type_as_string_values():
    trip_df = pl.DataFrame({"payment_type": [6, 5, 4, 3, 2, 1]})
    actual_df = update_payment_type_as_string_values(trip_df)

    expected_df = pl.DataFrame(
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

    assert_pl_frame_equal(actual_df, expected_df)


def test_add_borough_and_zone():
    trip_df = pl.DataFrame(
        {
            "pulocationid": [1, 2, 3, 4, 5],
            "dolocationid": [1, 2, 3, 4, 5],
        }
    )
    zone_df = pl.DataFrame(
        {
            "locationid": [1, 2, 3, 4, 5],
            "borough": ["Manhattan", "Queens", "Bronx", "Brooklyn", "Staten Island"],
            "zone": ["Midtown", "Astoria", "Riverdale", "Park Slope", "Tottenville"],
        }
    )

    actual_df = add_borough_and_zone(trip_df, zone_df, "pulocationid")
    expected_df = pl.DataFrame(
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


def test_calc_result_most_frequent_three_routes(locations):
    trip_df = pl.DataFrame(locations)
    actual_df = calc_result_most_frequent_three_routes(trip_df)

    expected_df = pl.DataFrame(
        {
            "pulocationid_borough": [
                "Manhattan",
                "Bronx",
                "Brooklyn",
            ],
            "pulocationid_zone": [
                "Upper East Side",
                "Riverdale",
                "Williamsburg",
            ],
            "dolocationid_borough": [
                "Queens",
                "Bronx",
                "Bronx",
            ],
            "dolocationid_zone": [
                "Astoria",
                "Fordham",
                "Riverdale",
            ],
            "num_trips": [3, 2, 2],
        }
    )
    assert_pl_frame_equal(actual_df, expected_df, check_row_order=False)


def test_calc_cash_journeys_per_pickup():
    trip_df = pl.DataFrame(
        {
            "payment_type": ["CASH", "CREDIT", "CASH", "NO_CHARGE", "CASH"],
            "pulocationid_borough": ["1", "2", "1", "3", "1"],
            "pulocationid_zone": ["1", "1", "1", "3", "4"],
        }
    )
    actual_df = calc_cash_journeys_per_pickup(trip_df)

    expected_df = pl.DataFrame(
        {
            "pulocationid_borough": ["1", "1"],
            "pulocationid_zone": ["1", "4"],
            "num_cash_journeys": [2, 1],
        }
    )

    assert_pl_frame_equal(actual_df, expected_df)


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

    trip_df = pl.DataFrame(locations_with_tolls)
    actual_df = calc_highest_tolls_per_route(trip_df)
    actual_df = actual_df.select("tolls_amount_sum")

    expected_df = pl.DataFrame(
        {"tolls_amount_sum": [3.0, 3.0, 2.0, 2.0, 1.0, 1.0, 1.0]}
    )

    assert_pl_frame_equal(actual_df, expected_df)
