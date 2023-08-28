import importlib
import pandas as pd
import polars as pl
import types

from enum import Enum
from pathlib import Path
from typing import Any, Dict

from ppp.util import DATA_PATH


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


SCHEMA_DICT = {
    "polars": {
        "VendorID": pl.Int64,
        "tpep_pickup_datetime": pl.Datetime(time_unit="ns", time_zone=None),
        "tpep_dropoff_datetime": pl.Datetime(time_unit="ns", time_zone=None),
        "passenger_count": pl.Int64,
        "trip_distance": pl.Float64,
        "RatecodeID": pl.Int64,
        "store_and_fwd_flag": pl.Utf8,
        "PULocationID": pl.Int64,
        "DOLocationID": pl.Int64,
        "payment_type": pl.Int64,
        "fare_amount": pl.Float64,
        "extra": pl.Float64,
        "mta_tax": pl.Float64,
        "tip_amount": pl.Float64,
        "tolls_amount": pl.Float64,
        "improvement_surcharge": pl.Float64,
        "total_amount": pl.Float64,
        "congestion_surcharge": pl.Float64,
        "airport_fee": pl.Float64,
    },
    "pandas": {
        "VendorID": "int64",
        "tpep_pickup_datetime": "datetime64[ns]",
        "tpep_dropoff_datetime": "datetime64[ns]",
        "passenger_count": "int64",
        "trip_distance": "float64",
        "RatecodeID": "int64",
        "store_and_fwd_flag": "object",
        "PULocationID": "int64",
        "DOLocationID": "int64",
        "payment_type": "int64",
        "fare_amount": "float64",
        "extra": "float64",
        "mta_tax": "float64",
        "tip_amount": "float64",
        "tolls_amount": "float64",
        "improvement_surcharge": "float64",
        "total_amount": "float64",
        "congestion_surcharge": "float64",
        "airport_fee": "float64",
    },
}


ROUTE_COLUMNS = [
    "pulocationid_borough",
    "pulocationid_zone",
    "dolocationid_borough",
    "dolocationid_zone",
]


def read_zone_lookup(config: Dict) -> Any:
    """
    Read zone lookup data from a CSV file using the path and API specified in the config file.

    Args:
        config (Dict): Configuration dictionary with "path" and "module" keys.

    Returns:
        Any: Data read from the CSV file using the specified API.
    """
    zone_lookup_csv_path = DATA_PATH / config["path"]["lookup_csv"]

    api_name = config["module"]["name"]
    api = importlib.import_module(api_name)
    return api.read_csv(zone_lookup_csv_path)


def read_parquet_files(config: Dict) -> Any:
    """
    Read and combine data from Parquet files. File paths and API are specified in config file.

    Args:
        config (Dict): Configuration dictionary with "path" and "module" keys.

    Returns:
        Any: List of DataFrames containing data from the Parquet files.
    """
    parquet_files_dict = config["path"]["parquet_files"]["data"]

    parquet_files = [
        DATA_PATH / year / file
        for year, file_list in parquet_files_dict.items()
        for file in file_list
    ]

    api_name = config["module"]["name"]
    api = importlib.import_module(api_name)

    dataframes = []
    for file in parquet_files:
        df = api.read_parquet(file)

        if api_name == "pandas":
            df_schema_corrected = df.astype(SCHEMA_DICT[api_name])
            dataframes.append(df_schema_corrected)
        elif api_name == "polars":
            df_schema_corrected = api.DataFrame(
                df.to_dict(), schema=SCHEMA_DICT[api_name]
            )
            dataframes.append(df_schema_corrected)

    return api.concat(dataframes)


def write_parquet_file(file_name: str, df: Any, config: Dict) -> None:
    """
    Write data to a Parquet file: ./data/file_name.parquet. API is specified in config file.

    Args:
        file_name (str): Name of the Parquet file (without extension).
        df (Any): DataFrame containing data to be written to Parquet file.
        config (Dict): Configuration dictionary with "path" and "module" keys.
    """
    parquet_file_path = DATA_PATH / str(file_name + ".parquet")

    api_name = config["module"]["name"]

    if api_name == "pandas":
        df.to_parquet(parquet_file_path)
    elif api_name == "polars":
        df.write_parquet(parquet_file_path)


def write_csv_file(file_name: str, df: Any, config: Dict) -> None:
    """
    Write data to a CSV file: ./data/file_name.csv. API is specified in config file.

    Args:
        file_name (str): Name of the CSV file (without extension).
        df (Any): DataFrame containing data to be written to CSV file.
        config (Dict): Configuration dictionary with "path" and "module" keys.
    """
    parquet_file_path = DATA_PATH / str(file_name + ".csv")

    api_name = config["module"]["name"]

    if api_name == "pandas":
        df.to_csv(parquet_file_path)
    elif api_name == "polars":
        df.write_csv(parquet_file_path)


def get_schema(df: Any, config: Dict) -> Dict:
    """
    Get schema of DataFrame. API is specified in config file.

    Args:
        df (Any): DataFrame whose schema is to be returned.
        config (Dict): Configuration dictionary with "module" key.

    Returns:
        Dict: Dictionary containing column names and data types.
    """
    api_name = config["module"]["name"]
    api = importlib.import_module(api_name)

    if api_name == "pandas":
        return df.dtypes.to_dict()
    elif api_name == "polars":
        return df.schema
