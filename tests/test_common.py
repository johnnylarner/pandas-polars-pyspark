import pytest
import numpy as np
import polars as pl

# from unittest.mock import Mock
# from src.ppp.common import read_parquet_file, read_csv_file

from src.ppp.common import get_schema


# TODO: test for read_zone_lookup
# TODO: test for read_parquet_files
# TODO: write test for write_csv_file
# TODO: write test for write_parquet_file


def test_get_schema_pandas(pandas_df):
    config = {"module": {"name": "pandas"}}
    expected_schema = {"col1": np.int64, "col2": object}

    schema = get_schema(pandas_df, config)

    assert schema == expected_schema


def test_get_schema_polars(polars_df):
    config = {"module": {"name": "polars"}}
    expected_schema = {"col1": pl.Int64, "col2": pl.Utf8}

    schema = get_schema(polars_df, config)

    assert schema == expected_schema
