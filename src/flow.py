import os
import shutil

from prefect import flow, task
from prefect.assets import materialize
from prefect.task_runners import ThreadPoolTaskRunner
from prefect.futures import wait
from pathlib import Path

from src.osm import get_uk_regions, download_hospitals, HospitalsSource
from src.s3 import upload_to_s3, list_s3_objects, download_from_s3
from src.transformations import process_raw_hospitals_data

@task(
    tags=["api_rate_limit"],
    task_run_name="extract_{region[county]}",
 )
def extract_region_hospitals(region: dict[str, str]) -> Path:
    geojson_path = download_hospitals(region, source=HospitalsSource.OSM)
    return geojson_path

@task
def load_bronze(geojson_path: Path, bucket: str) -> str:
    s3_key = geojson_path.name
    upload_to_s3(bucket, s3_key, geojson_path)
    return s3_key

@flow(task_runner=ThreadPoolTaskRunner(max_workers=3))
def extract_hospitals_flow(bucket: str):
    regions = list(get_uk_regions())
    geojsons = extract_region_hospitals.map(regions)
    futures = load_bronze.map(geojson_path=geojsons, bucket=bucket)

    wait(futures)

@task
def get_geojson_list(bucket: str) -> list[str]:
    return list_s3_objects(bucket)

@task
def get_geojsons(key: str, bucket: str) -> Path:
    local_path = Path(f"data/{key}")
    download_from_s3(bucket, key, local_path)
    return local_path

@task
def transform_hospitals(geojson_path: list[Path]) -> Path:
    parquet_path = Path("hospitals.geoparquet")
    process_raw_hospitals_data(geojson_path, parquet_path)
    return parquet_path

@materialize("s3://bucket/hospitals.geoparquet")
def load_silver(parquet_path: Path, bucket: str) -> str:
    s3_key = parquet_path.name
    upload_to_s3(bucket, s3_key, parquet_path)
    return s3_key

@flow(task_runner=ThreadPoolTaskRunner(max_workers=10))
def transform_hospitals_flow(bronze_bucket: str, silver_bucket: str):
    geojson_keys = get_geojson_list(bronze_bucket)

    os.makedirs("data", exist_ok=True)
    geojsons = get_geojsons.map(geojson_keys, bucket=bronze_bucket)

    parquet_path = transform_hospitals(geojsons)
    if parquet_path is not None:
        load_hospitals = load_silver
        load_hospitals.with_options(
            assets=[f"s3://{silver_bucket}/{parquet_path.name}"],
        )
        load_hospitals(parquet_path, bucket=silver_bucket)

    shutil.rmtree("data")
