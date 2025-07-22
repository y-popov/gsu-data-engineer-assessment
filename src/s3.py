import boto3
from pathlib import Path

def upload_to_s3(bucket: str, key: str, path: Path):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).upload_file(Key=key, Filename=path)

def download_from_s3(bucket: str, key: str, path: Path):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).download_file(Key=key, Filename=path)

def list_s3_objects(bucket: str) -> list[str]:
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket)

    if 'Contents' not in response:
        return []

    return [obj['Key'] for obj in response['Contents']]
