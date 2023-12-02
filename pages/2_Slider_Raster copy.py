import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import streamlit as st 
from localtileserver import get_leaflet_tile_layer, TileClient
from ipyleaflet import Map

st.set_page_config(
    page_title="Slider",
    page_icon="🗺️",
)


day = st.slider('witch day', 0, 6, 2)
option = st.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'precipitation'))

# Load your GeoDataFrame from Parquet (assuming it has geometry columns)
gdf = gpd.read_parquet('waaaa.geoparquet')

# List of attribute columns
temp_attributes = ['temp_j0', 'temp_j1', 'temp_j2','temp_j3', 'temp_j4', 'temp_j5','temp_j6']
humd_attributes = ['humd_0', 'humd_1', 'humd_2','humd_3', 'humd_4', 'humd_5', 'humd_6']
preci_attributes = ['preci_0', 'preci_1', 'preci_2','preci_3', 'preci_4', 'preci_5', 'preci_6']

d=""
def att(value):
    if value== 'temperature':
        d="temp_j"
    if value== 'humidite':
        d="humd_"
    if value== 'precipitation':
        d="preci_"
    return d 

try:
    # First, create a tile server from local raster file
    client = TileClient("{}cp.tif".format(str(att(option))+str(day)))
    # client = TileClient("/content/drive/MyDrive/AAAA/tif1.tif")
    # Create ipyleaflet tile layer from that server
    t = get_leaflet_tile_layer(client)
    m = Map(center=client.center(), zoom=client.default_zoom)
    m.add_layer(t)


    
except Exception as e:
    print(f"Error creating tile layer for client2: {e}")
    import traceback
    traceback.print_exc()
