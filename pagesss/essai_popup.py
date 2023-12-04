import streamlit
import geopandas as gpd
import matplotlib.pyplot as plt
import geopandas as gpd
import folium
from streamlit_folium import folium_static

# File path
points_fp = "waaaa.geoparquet"

# Read the data
data = gpd.read_parquet(points_fp)

#Check input data
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)

points_gjson = folium.features.GeoJson(gdf, name="Public transport stations")

# Create a Map instance
m = folium.Map(location=[34, -5], tiles = 'cartodbpositron', zoom_start=11, control_scale=True)

# Add points to the map instance
points_gjson.add_to(m)

# Alternative syntax for adding points to the map instance
#m.add_child(points_gjson)


folium_static(m)