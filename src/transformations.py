import geopandas as gpd
from pathlib import Path

def clean_hospitals(gdf: gpd.GeoDataFrame):
    gdf["addr:country"].fillna("GB", inplace=True)
    return

def process_raw_hospitals_data(input: Path, output: Path):
    """
    Takes a path to GeoJSON file, cleans it, transforms into GeoParquet and saves under given path.
    """
    gdf = gpd.read_file(input)
    clean_hospitals(gdf)
    gdf.to_parquet(output)
