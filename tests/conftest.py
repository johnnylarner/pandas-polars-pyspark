import io
import os
from typing import Any, Callable
from unittest.mock import MagicMock

import aiobotocore.awsrequest
import aiobotocore.endpoint
import aiohttp
import aiohttp.client_reqrep
import aiohttp.typedefs
import boto3
import botocore.awsrequest
import botocore.model
import polars as pl
import pytest
from moto import mock_s3


def write_df_to_bytes_buffer(df: pl.DataFrame) -> io.BytesIO:
    """
    Write a DataFrame to a bytes buffer.
    """
    buffer = io.BytesIO()
    df.write_parquet(buffer)
    buffer.seek(0)
    return buffer


class MockAWSResponse(aiobotocore.awsrequest.AioAWSResponse):
    """
    Mocked AWS Response.

    https://github.com/aio-libs/aiobotocore/issues/755
    https://gist.github.com/giles-betteromics/12e68b88e261402fbe31c2e918ea4168
    """

    def __init__(self, response: botocore.awsrequest.AWSResponse):
        self._moto_response = response
        self.status_code = response.status_code
        self.raw = MockHttpClientResponse(response)

    # adapt async methods to use moto's response
    async def _content_prop(self) -> bytes:
        return self._moto_response.content

    async def _text_prop(self) -> str:
        return self._moto_response.text


class MockHttpClientResponse(aiohttp.client_reqrep.ClientResponse):
    """
    Mocked HTP Response.

    See <MockAWSResponse> Notes
    """

    def __init__(self, response: botocore.awsrequest.AWSResponse):
        """
        Mocked Response Init.
        """

        async def read(self: MockHttpClientResponse, n: int = -1) -> bytes:
            return response.content

        self.content = MagicMock(aiohttp.StreamReader)
        self.content.read = read
        self.response = response

    @property
    def raw_headers(self) -> Any:
        """
        Return the headers encoded the way that aiobotocore expects them.
        """
        return {
            k.encode("utf-8"): str(v).encode("utf-8")
            for k, v in self.response.headers.items()
        }.items()


@pytest.fixture(scope="session", autouse=True)
def patch_aiobotocore() -> None:
    """
    Pytest Fixture Supporting S3FS Mocks.

    See <MockAWSResponse> Notes
    """

    def factory(original: Callable[[Any, Any], Any]) -> Callable[[Any, Any], Any]:
        """
        Response Conversion Factory.
        """

        def patched_convert_to_response_dict(
            http_response: botocore.awsrequest.AWSResponse,
            operation_model: botocore.model.OperationModel,
        ) -> Any:
            return original(MockAWSResponse(http_response), operation_model)

        return patched_convert_to_response_dict

    aiobotocore.endpoint.convert_to_response_dict = factory(
        aiobotocore.endpoint.convert_to_response_dict
    )


@pytest.fixture(scope="session")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="session")
def bucket_config():
    return {"Bucket": "test-bucket", "Key": "data"}


@pytest.fixture(scope="session", autouse=True)
def s3(aws_credentials):
    with mock_s3():
        yield boto3.client("s3")


@pytest.fixture(scope="session", autouse=True)
def s3_bucket(s3, bucket_config):
    s3.create_bucket(Bucket=bucket_config["Bucket"])
    yield


@pytest.fixture(scope="session")
def s3_data(s3, bucket_config):
    print("Setting up dummy S3 bucket with parquet data")
    dummy_parquet_df = pl.DataFrame({"a": [1, 2, 3]})

    partitions = ["year=2020", "year=2021"]
    for partition in partitions:
        buffer = write_df_to_bytes_buffer(dummy_parquet_df)

        partition_key = f"{bucket_config['Key']}/{partition}/data.parquet"
        s3.put_object(Bucket=bucket_config["Bucket"], Key=partition_key, Body=buffer)


@pytest.fixture(scope="session")
def s3_data_uri(s3_data, bucket_config):
    return "s3://{Bucket}/{Key}".format(**bucket_config)


@pytest.fixture(scope="module")
def locations():
    return {
        "pulocationid_borough": [
            "Manhattan",
            "Manhattan",
            "Manhattan",
            "Queens",
            "Queens",
            "Bronx",
            "Bronx",
            "Brooklyn",
            "Brooklyn",
            "Brooklyn",
            "Unknown",
            "Unknown",
            "Unknown",
        ],
        "pulocationid_zone": [
            "Upper East Side",
            "Upper East Side",
            "Upper East Side",
            "Astoria",
            "Hunters Point",
            "Riverdale",
            "Riverdale",
            "Williamsburg",
            "Williamsburg",
            "Bushwick",
            "Unknown",
            "Unknown",
            "Unknown",
        ],
        "dolocationid_borough": [
            "Queens",
            "Queens",
            "Queens",
            "Manhattan",
            "Manhattan",
            "Bronx",
            "Bronx",
            "Bronx",
            "Bronx",
            "Bronx",
            "Unknown",
            "Unknown",
            "Unknown",
        ],
        "dolocationid_zone": [
            "Astoria",
            "Astoria",
            "Astoria",
            "Upper East Side",
            "Lower East Side",
            "Fordham",
            "Fordham",
            "Riverdale",
            "Riverdale",
            "Riverdale",
            "Unknown",
            "Unknown",
            "Unknown",
        ],
    }


@pytest.fixture(scope="module")
def top3_locations():
    return {
        "pulocationid_borough": [
            "Manhattan",
            "Bronx",
            "Brooklyn",
        ],
        "pulocationid_zone": [
            "Upper East Side",
            "Riverdale",
            "Williamsburg",
        ],
        "dolocationid_borough": [
            "Queens",
            "Bronx",
            "Bronx",
        ],
        "dolocationid_zone": [
            "Astoria",
            "Fordham",
            "Riverdale",
        ],
        "num_trips": [3, 2, 2],
    }
