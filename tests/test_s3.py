import boto3
import tempfile
import pytest

from pathlib import Path
from moto import mock_aws

from src.s3 import *

@pytest.fixture
def s3():
    with mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        bucket = "my-bucket"
        s3.create_bucket(Bucket=bucket)
        yield s3, bucket

def test_download_from_s3(s3):
    client, bucket = s3

    filekey = "test.txt"
    client.put_object(Bucket=bucket, Key=filekey, Body=b"content")

    with tempfile.NamedTemporaryFile(delete=True) as f:
        output = Path(f.name)
        download_from_s3(bucket, filekey, output)
        data = output.read_text()

    assert data == "content"

def test_upload_to_s3(s3):
    client, bucket = s3

    filekey = "test.txt"
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        f.write("content")
        temp_path = Path(f.name)

    upload_to_s3(bucket, filekey, temp_path)
    temp_path.unlink()

    response = client.get_object(Bucket=bucket, Key=filekey)
    assert response["Body"].read() == b"content"

def test_list_s3_objects(s3):
    client, bucket = s3

    filekey1 = "test1.txt"
    filekey2 = "test2.txt"
    client.put_object(Bucket=bucket, Key=filekey1, Body=b"content1")
    client.put_object(Bucket=bucket, Key=filekey2, Body=b"content2")

    objects = list_s3_objects(bucket)
    assert set(objects) == {filekey1, filekey2}
