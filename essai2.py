import streamlit as st
import pandas as pd 
import numpy as np
import pydeck as pdk
import geopandas as gpd
import folium
import geemap.foliumap as geemap
from localtileserver.widgets import get_folium_tile_layer
import streamlit as st
import folium
from streamlit_folium import folium_static
from PIL import Image
import numpy as np
from folium import plugins
import rasterio
from rasterio.warp import transform_bounds
import leafmap.foliumap as leafmap
from altair import Chart

import vega_datasets

datafile ='waaaa.geoparquet'
#on lit notre fichier geoparquet
data = pd.read_parquet(datafile)
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)

# load built-in dataset as a pandas DataFrame
# cars = vega_datasets.data.cars()
# print(cars)

gdf = pd.DataFrame(data)

i = 0
for i in gdf :

    # Place the markers with the popup labels and data
    map.add_child(
        folium.Marker(
            location='[longitude, latitude]',
            popup="Year: "
            ,
            icon=folium.Icon(color="red"),
        )
    )
    i = i + 1
folium_static(map)