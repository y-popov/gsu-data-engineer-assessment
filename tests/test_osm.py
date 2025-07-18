import pytest
from geopandas import GeoDataFrame

from src.osm import *

example_data = {
    "county": "rutland",
    "name": "rutland-latest.osm.pbf",
    "url": "http://download.geofabrik.de/europe/united-kingdom/england/rutland-latest.osm.pbf"
}

def test_get_uk_regions():
    regions = list(get_uk_regions())

    assert len(regions) == 49

    counties = [x["county"] for x in regions]
    assert "wales" in counties
    assert "cambridgeshire" in counties
    assert "england" not in counties

def test_download_from_geofabrik():
    file = download_pbf_from_geofabrik(example_data)

    assert file.exists()
    assert file.name == example_data["name"]

    hospitals = extract_hospitals_from_pbf(file)
    assert isinstance(hospitals, GeoDataFrame)

    file.unlink()

def test_download_hospitals_from_osm():
    hospitals = download_hospitals_from_osm(example_data["county"])
    assert isinstance(hospitals, GeoDataFrame)

@pytest.mark.parametrize("source", [HospitalsSource.OSM, HospitalsSource.GeoFabrik])
def test_download_hospitals(source):
    file = download_hospitals(example_data, source)
    assert file.exists()
    assert file.suffix == ".geojson"
    file.unlink()
