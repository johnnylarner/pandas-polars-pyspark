import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from ppp.pandas import (
    add_features,
    rename_columns_as_lowercase,
)


def test_hallo_welt():
    print("Hallo Welt!")


# def test_dev():
#     __import__("IPython").embed()


# unit test that tests function rename_columns_as_lowercase
def test_rename_columns_as_lowercase():
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    expected = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

    result = rename_columns_as_lowercase(df)

    assert_frame_equal(result, expected)
