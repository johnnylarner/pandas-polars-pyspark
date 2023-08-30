import pytest
import numpy as np
import polars as pl

from unittest.mock import Mock

from src.ppp.common import get_schema, write_csv_file, write_parquet_file


# TODO: test for read_zone_lookup
# TODO: test for read_parquet_files


def test_write_parquet_file_with_pandas(mock_data_frame, data_path):
    file_name = "test_file"
    parquet_file_path = data_path / str(file_name + ".parquet")

    config = {"module": {"name": "pandas"}}

    write_parquet_file(file_name, mock_data_frame, config)

    assert mock_data_frame.to_parquet.called_once_with(parquet_file_path)


def test_write_parquet_file_with_polars(mock_data_frame, data_path):
    file_name = "test_file"
    parquet_file_path = data_path / str(file_name + ".parquet")

    config = {"module": {"name": "polars"}}

    write_parquet_file(file_name, mock_data_frame, config)

    assert mock_data_frame.to_parquet.called_once_with(parquet_file_path)


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


# from src.ppp.common import read_parquet_file, read_csv_file


# def test_read_zone_lookup_pandas(pandas_api_mock):
#     config = {
#         "path": {
#             "lookup_csv": "zone_lookup.csv"
#         },
#         "module": {
#             "name": "pandas_api"  # Mocked module name for pandas
#         }
#     }

#     result = read_zone_lookup(config)

#     assert result == pandas_api_mock.read_csv.return_value

# def test_read_zone_lookup_polars(polars_api_mock):
#     config = {
#         "path": {
#             "lookup_csv": "zone_lookup.csv"
#         },
#         "module": {
#             "name": "polars_api"  # Mocked module name for polars
#         }
#     }

#     result = read_zone_lookup(config)

#     assert result == polars_api_mock.read_csv.return_value


# def test_read_parquet_pandas(monkeypatch):
#     # Mock pandas module with a mock read_parquet method
#     pandas_mock = Mock()
#     pandas_mock.read_parquet.return_value = "Pandas DataFrame"

#     # Mock importlib.import_module to return the mock pandas module
#     monkeypatch.setattr(
#         "scripts.feature_engineering.importlib.import_module", lambda _: pandas_mock
#     )

#     result = read_parquet_file("path/to/file.parquet", "pandas")

#     assert result == "Pandas DataFrame"
#     pandas_mock.read_parquet.assert_called_once_with("path/to/file.parquet")


# def test_read_parquet_polars(monkeypatch):
#     # Mock polars module with a mock read_parquet method
#     polars_mock = Mock()
#     polars_mock.read_parquet.return_value = "Polars DataFrame"

#     # Mock importlib.import_module to return the mock polars module
#     monkeypatch.setattr(
#         "scripts.feature_engineering.importlib.import_module", lambda _: polars_mock
#     )

#     result = read_parquet_file("path/to/file.parquet", "polars")

#     assert result == "Polars DataFrame"
#     polars_mock.read_parquet.assert_called_once_with("path/to/file.parquet")


# def test_read_csv_pandas(monkeypatch):
#     # Mock pandas module with a mock read_csv method
#     pandas_mock = Mock()
#     pandas_mock.read_csv.return_value = "Pandas DataFrame"

#     # Mock importlib.import_module to return the mock pandas module
#     monkeypatch.setattr(
#         "scripts.feature_engineering.importlib.import_module", lambda _: pandas_mock
#     )

#     result = read_csv_file("path/to/file.csv", "pandas")

#     assert result == "Pandas DataFrame"
#     pandas_mock.read_csv.assert_called_once_with("path/to/file.csv")


# def test_read_csv_polars(monkeypatch):
#     # Mock polars module with a mock read_csv method
#     polars_mock = Mock()
#     polars_mock.read_csv.return_value = "Polars DataFrame"

#     # Mock importlib.import_module to return the mock polars module
#     monkeypatch.setattr(
#         "scripts.feature_engineering.importlib.import_module", lambda _: polars_mock
#     )

#     result = read_csv_file("path/to/file.csv", "polars")

#     assert result == "Polars DataFrame"
#     polars_mock.read_csv.assert_called_once_with("path/to/file.csv")
