import boto3
import tempfile
import pytest

from pathlib import Path
from moto import mock_aws

from src.s3 import download_from_s3, upload_to_s3

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