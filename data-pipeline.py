import os

from prefect import flow, task
from prefect.task_runners import ThreadPoolTaskRunner
from prefect.futures import wait
from prefect import get_client
from pathlib import Path

from src.osm import get_uk_regions, download_hospitals, HospitalsSource
from src.s3 import upload_to_s3
from src.transformations import process_raw_hospitals_data

BRONZE_BUCKET = os.getenv("TF_VAR_bronze_bucket")
SILVER_BUCKET = os.getenv("TF_VAR_silver_bucket")

@task(tags=["api_rate_limit"])
def extract_region_hospitals(region):
    geojson_path = download_hospitals(region, source=HospitalsSource.OSM)
    return geojson_path

@task
def load_bronze(geojson_path: Path):
    s3_key = geojson_path.name
    upload_to_s3(BRONZE_BUCKET, s3_key, geojson_path)
    return s3_key

@task
def transform_hospitals(geojson_path: Path):
    parquet_path = geojson_path.with_suffix(".geoparquet")
    process_raw_hospitals_data(geojson_path, parquet_path)
    return parquet_path

@task
def load_silver(parquet_path: Path):
    s3_key = parquet_path.name
    upload_to_s3(SILVER_BUCKET, s3_key, parquet_path)
    return s3_key

@flow(task_runner=ThreadPoolTaskRunner(max_workers=3))
def hospital_pipeline():
    regions = list(get_uk_regions())[:3]
    geojsons = extract_region_hospitals.map(regions)
    futures = load_bronze.map(geojsons)

    wait(futures)

        # parquet_path = transform_hospitals(geojson_path)
        # load_silver(parquet_path)

if __name__ == '__main__':
    hospital_pipeline()
