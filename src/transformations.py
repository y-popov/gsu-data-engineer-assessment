import geopandas as gpd
from pathlib import Path

def clean_hospitals(gdf: gpd.GeoDataFrame):
    gdf = gdf.drop_duplicates(subset=["id"], keep="first")

    # Fill missing values
    rules = {
        "addr:country": "GB",
    }

    if "postal_code" in gdf.columns:
        rules["addr:postcode"] = gdf["postal_code"]

    for rule in ["contact:phone", "contact:website","contact:email"]:
        field = rule.split(":")[1]
        if field in gdf.columns:
            rules[rule] = gdf["field"]

    gdf = gdf.fillna(rules)

    # Remove unwanted columns
    col_whitelist = ["id", "name", "amenity", "element", "geometry"]
    col_whitelist.extend(gdf.columns[gdf.columns.str.startswith("addr:")])
    col_whitelist.extend(gdf.columns[gdf.columns.str.startswith("contact:")])
    gdf = gdf[col_whitelist]

    # TODO fill-in missing addresses using reverse geocoding
    # https://developers.google.com/maps/documentation/geocoding/overview

    return gdf

def process_raw_hospitals_data(input: list[Path], output: Path):
    """
    Takes a list of GeoJSON files, cleans it, transforms into GeoParquet and saves under given path.
    """
    gdf = gpd.pd.concat(map(gpd.read_file, input), ignore_index=True)
    gdf = clean_hospitals(gdf)
    gdf.to_parquet(output)
