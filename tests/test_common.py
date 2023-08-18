import pytest
from unittest.mock import Mock
from src.ppp.common import read_parquet_file, read_csv_file


def test_read_parquet_pandas(monkeypatch):
    # Mock pandas module with a mock read_parquet method
    pandas_mock = Mock()
    pandas_mock.read_parquet.return_value = "Pandas DataFrame"

    # Mock importlib.import_module to return the mock pandas module
    monkeypatch.setattr(
        "scripts.feature_engineering.importlib.import_module", lambda _: pandas_mock
    )

    result = read_parquet_file("path/to/file.parquet", "pandas")

    assert result == "Pandas DataFrame"
    pandas_mock.read_parquet.assert_called_once_with("path/to/file.parquet")


def test_read_parquet_polars(monkeypatch):
    # Mock polars module with a mock read_parquet method
    polars_mock = Mock()
    polars_mock.read_parquet.return_value = "Polars DataFrame"

    # Mock importlib.import_module to return the mock polars module
    monkeypatch.setattr(
        "scripts.feature_engineering.importlib.import_module", lambda _: polars_mock
    )

    result = read_parquet_file("path/to/file.parquet", "polars")

    assert result == "Polars DataFrame"
    polars_mock.read_parquet.assert_called_once_with("path/to/file.parquet")


def test_module_not_found():
    with pytest.raises(ValueError):
        read_parquet_file("path/to/file.parquet", "nonexistent_module")


def test_read_csv_pandas(monkeypatch):
    # Mock pandas module with a mock read_csv method
    pandas_mock = Mock()
    pandas_mock.read_csv.return_value = "Pandas DataFrame"

    # Mock importlib.import_module to return the mock pandas module
    monkeypatch.setattr(
        "scripts.feature_engineering.importlib.import_module", lambda _: pandas_mock
    )

    result = read_csv_file("path/to/file.csv", "pandas")

    assert result == "Pandas DataFrame"
    pandas_mock.read_csv.assert_called_once_with("path/to/file.csv")


def test_read_csv_polars(monkeypatch):
    # Mock polars module with a mock read_csv method
    polars_mock = Mock()
    polars_mock.read_csv.return_value = "Polars DataFrame"

    # Mock importlib.import_module to return the mock polars module
    monkeypatch.setattr(
        "scripts.feature_engineering.importlib.import_module", lambda _: polars_mock
    )

    result = read_csv_file("path/to/file.csv", "polars")

    assert result == "Polars DataFrame"
    polars_mock.read_csv.assert_called_once_with("path/to/file.csv")
