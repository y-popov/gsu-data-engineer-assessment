import boto3
import os
from pathlib import Path

def upload_to_s3(bucket: str, key: str, path: Path):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).upload_file(Key=key, Filename=path)

def download_from_s3(bucket: str, key: str, path: Path):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).download_file(Key=key, Filename=path)
