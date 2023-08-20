import pytest
import types

from ppp.util import get_resource_string, import_module


def test_get_resource_string():
    s = get_resource_string("version.py")
    assert "__version__ = " in s


def test_import_pandas():
    config = {"module": {"name": "pandas"}}

    mod = import_module(config)

    assert hasattr(mod, "add_features")
    assert callable(mod.add_features)


def test_import_polars():
    config = {"module": {"name": "polars"}}

    mod = import_module(config)

    assert hasattr(mod, "add_features")
    assert callable(mod.add_features)


def test_import_nonexistent_module():
    config = {"module": {"name": "nonexistent_module"}}

    with pytest.raises(ValueError) as excinfo:
        import_module(config)

    assert f"Module '{config['module']['name']}' not found." in str(excinfo.value)
