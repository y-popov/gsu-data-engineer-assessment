import tempfile
import osmnx as ox
import pyrosm

from enum import Enum
from pathlib import Path
from geopandas import GeoDataFrame


def download_hospitals_from_osm(county: str) -> GeoDataFrame:
    hospitals = ox.features_from_place(f"{county}, United Kingdom", tags={"amenity": "hospital"})
    return hospitals

def get_uk_regions():
    regions = pyrosm.data.sources.subregions.great_britain.regions
    for region in regions:
        region_data = getattr(pyrosm.data.sources.subregions.great_britain, region)
        if isinstance(region_data, dict):
            subregions = [region]
        else:
            subregions = getattr(pyrosm.data.sources.subregions.great_britain, region).regions

        for subregion in subregions:
            data =  pyrosm.data.sources.subregions.great_britain.__dict__[subregion]
            data['county'] = subregion
            if subregion.endswith("_with_hull"):
                data['county'] = subregion.replace("_with_hull", "")
            yield data


def download_pbf_from_geofabrik(data: dict[str, str]) -> Path:
    uk_fix = {"europe/great-britain/": "europe/united-kingdom/"}

    for old, new in uk_fix.items():
        data["url"] = data["url"].replace(old, new)

    filename = pyrosm.data.retrieve(data, update=False, directory=tempfile.gettempdir())
    return Path(filename)

def extract_hospitals_from_pbf(path: Path) -> GeoDataFrame:
    osm = pyrosm.OSM(str(path))
    hospitals = osm.get_pois(custom_filter={"amenity": ["hospital"]})
    return hospitals

def download_hospitals_from_geofabrik(data: dict[str, str]) -> GeoDataFrame:
    file = download_pbf_from_geofabrik(data)
    hospitals = extract_hospitals_from_pbf(file)
    file.unlink()
    return hospitals


class HospitalsSource(Enum):
    OSM = "osm"
    GeoFabrik = "geofabrik"

def download_hospitals(county_data: dict[str, str], source: HospitalsSource) -> Path:
    """
    Downloads hospitals data from specified source for the given county, saves it as GeoJson and returns path to it.
    """
    county_name = county_data["county"]

    if source == HospitalsSource.OSM:
        hospitals = download_hospitals_from_osm(county_name)
    elif source == HospitalsSource.GeoFabrik:
        hospitals = download_hospitals_from_geofabrik(county_data)
    else:
        raise ValueError(f"Unknown source: {source}")

    file = Path(tempfile.gettempdir()) / f"{county_name}.geojson"
    hospitals.to_file(file, driver='GeoJSON')

    return file