from src.osm import get_uk_regions, download_hospitals, HospitalsSource

if __name__ == '__main__':
    for uk_region in get_uk_regions():
        hospitals = download_hospitals(uk_region, source=HospitalsSource.GeoFabrik)

