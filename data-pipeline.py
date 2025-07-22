import os

from src.flow import extract_hospitals_flow, transform_hospitals_flow

BRONZE_BUCKET = os.getenv("TF_VAR_bronze_bucket")
SILVER_BUCKET = os.getenv("TF_VAR_silver_bucket")

if __name__ == '__main__':
    assert BRONZE_BUCKET is not None
    assert SILVER_BUCKET is not None

    # TODO add CLI to run the specific flow
    extract_hospitals_flow(BRONZE_BUCKET)
    transform_hospitals_flow(BRONZE_BUCKET, SILVER_BUCKET)
