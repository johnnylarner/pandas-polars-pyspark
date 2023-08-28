import pytest


@pytest.fixture(scope="module")
def pandas_df():
    import pandas as pd

    data = {"col1": [1, 2, 3], "col2": ["a", "b", "c"]}
    return pd.DataFrame(data)


@pytest.fixture(scope="module")
def polars_df():
    import polars as pl

    data = {"col1": [1, 2, 3], "col2": ["a", "b", "c"]}
    return pl.DataFrame(data)


@pytest.fixture(scope="module")
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


@pytest.fixture(scope="module")
def top3_locations():
    return {
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
