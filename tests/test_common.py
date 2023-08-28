import pytest
import numpy as np
import polars as pl

from unittest.mock import Mock


from src.ppp.common import get_schema, write_csv_file


# TODO: test for read_zone_lookup
# TODO: test for read_parquet_files
# TODO: write test for write_parquet_file


def test_write_csv_pandas(mock_data_frame):
    mock_data_frame.to_csv = Mock()
    mock_data_frame.write_csv = Mock()
    config = {"module": {"name": "pandas"}}
    file_name = "test_file"

    write_csv_file(file_name, mock_data_frame, config)

    assert mock_data_frame.to_csv.call_count == 1
    assert mock_data_frame.write_csv.call_count == 0


def test_write_csv_polars(mock_data_frame):
    mock_data_frame.to_csv = Mock()
    mock_data_frame.write_csv = Mock()
    config = {"module": {"name": "polars"}}
    file_name = "test_file"

    write_csv_file(file_name, mock_data_frame, config)

    assert mock_data_frame.to_csv.call_count == 0
    assert mock_data_frame.write_csv.call_count == 1


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
