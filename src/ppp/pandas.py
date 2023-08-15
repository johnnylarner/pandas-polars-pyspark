import pandas as pd
from pandas import DataFrame


def add_features(trip_df: DataFrame, zone_df: DataFrame) -> DataFrame:
    """Returns a pandas DataFrame containing
    all the features derived from NYC
    Taxi dataset to answer all business questions.
    """
    # TODO: a tuple[DataFrame, DataFrame] as a return value would be better but Process is killed
    # MB resident memory
    print("# resident memory before rename_columns_as_lowercase [MB]")
    import os, psutil

    print(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024))
    trip_df = rename_columns_as_lowercase(trip_df)
    # MB resident memory
    print("# resident memory after rename_columns_as_lowercase [MB]")
    print(psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024))
    # zone_df = rename_columns_as_lowercase(zone_df)

    return trip_df


def rename_columns_as_lowercase(df: DataFrame) -> DataFrame:
    """Returns a pandas DataFrame containing
    the df DataFrame with all columns
    renamed to be lowercase.
    """

    return df.rename({col: col.lower() for col in df.columns})


#
