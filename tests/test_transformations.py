import tempfile
import pytest

from src.transformations import *

@pytest.fixture(scope='module')
def sample_geojson():
    # return Path('data/hospitals.geojson')
    return Path('data/cambs.geojson')

def test_process_raw_hospitals_data(sample_geojson):
    with tempfile.NamedTemporaryFile(suffix=".geoparquet", delete=False) as f:
        output = Path(f.name)
        process_raw_hospitals_data(input=sample_geojson, output=output)
    output.unlink()
