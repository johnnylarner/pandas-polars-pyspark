import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Union

import pkg_resources
import psutil
import yaml
from cloudpathlib import S3Path

logger = logging.getLogger("ppp")

ROOT = Path(__file__).parent.parent.parent
CONFIG_PATH = ROOT / "config" / "config.yml"
DATA_PATH = ROOT / "data"
TERRAFORM_PATH = ROOT / "terraform"


def get_resource_string(path: str, decode=True) -> Union[str, bytes]:
    """
    Load a package resource (i.e. a file from within this package)

    :param path: the path, starting at the root of the current module (e.g. 'res/default.conf').
           must be a string, not a Path object!
    :param decode: if true, decode the file contents as string (otherwise return bytes)
    :return: the contents of the resource file (as string or bytes)
    """
    s = pkg_resources.resource_string(__name__.split(".")[0], path)
    return s.decode(errors="ignore") if decode else s


def get_resource_name_from_terraform(resource_name: str, terraform_dir: Path) -> str:
    """Returns the bucket name from the terraform state file."""
    logger.debug("Getting %s from terraform state", resource_name)

    resource = subprocess.check_output(
        f" terraform -chdir={terraform_dir} output -raw {resource_name}",
        shell=True,
    ).decode("utf-8")

    logger.debug("Got %s from terraform state", resource_name)
    return resource


def build_path_from_config(
    type: str, config: dict[str, dict[str, str]]
) -> Path | S3Path:
    if type == "local":
        return DATA_PATH
    elif type == "s3":
        s3_config = config["s3"]
        return S3Path(f"s3://{s3_config['bucket']}/{s3_config['key']}")


def load_config(config_file: Union[str, Path]) -> Dict[str, Any]:
    """
    Load the config from the specified yaml file

    :param config_file: path of the config file to load
    :return: the parsed config as dictionary
    """
    with open(config_file, "r") as fp:
        return yaml.safe_load(fp)


def logging_setup(config: Dict):
    """
    setup logging based on the configuration

    :param config: the parsed config tree
    """
    log_conf = config["logging"]
    fmt = log_conf["format"]
    if log_conf["enabled"]:
        level = logging._nameToLevel[log_conf["level"].upper()]
    else:
        level = logging.NOTSET
    logging.basicConfig(format=fmt, level=logging.WARNING)
    logger.setLevel(level)
    return logger


def get_rss() -> float:
    """calc RSS (resident set size) in bytes and transform it to Kilobyte"""
    return psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
