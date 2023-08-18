from enum import Enum
from typing import Any


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


ROUTE_COLUMNS = [
    "pulocationid_borough",
    "pulocationid_zone",
    "dolocationid_borough",
    "dolocationid_zone",
]


def read_parquet_file(path: str, module: str) -> Any:
    """
    Read a Parquet file using the specified module's read_parquet method.

    Args:
        path (str): Path to the Parquet file.
        module: The module (e.g., pandas, polars) that provides the read_parquet method.

    Returns:
        DataFrame: A DataFrame containing the data from the Parquet file.
    """
    try:
        import importlib

        mod = importlib.import_module(module)
        df = mod.read_parquet(path)

        return df
    except ImportError:
        raise ValueError(
            f"Module '{module}' not found or does not support read_parquet."
        )


def read_csv_file(path: str, module: str) -> Any:
    """
    Read a CSV file using the specified module's read_csv method.

    Args:
        path (str): Path to the CSV file.
        module: The module (e.g., pandas, polars) that provides the read_csv method.

    Returns:
        DataFrame: A DataFrame containing the data from the CSV file.
    """
    try:
        import importlib

        mod = importlib.import_module(module)
        df = mod.read_csv(path)

        return df
    except ImportError:
        raise ValueError(f"Module '{module}' not found or does not support read_csv.")
