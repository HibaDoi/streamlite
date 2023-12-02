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
import json
import ipywidgets
from lonboard import Map, ScatterplotLayer
from lonboard.colormap import apply_continuous_cmap
st.set_page_config(
    page_title="Volet Cartographie",
    page_icon="🗺️",
)


#on ajoute notre fichier geoparquet
datafile ='complet.geoparquet'
#on lit notre fichier geoparquet
data = pd.read_parquet(datafile)
#on ajoute un titre a notre page
st.header("station de meteo")
#add raw data table
if st.checkbox('show raw data'):
    st.subheader('raw data')
    st.write(data)
#on affiche la map
#st.map(data)
#on affiche avec symbologie
# Ici on a trouver une erreur dans laquel on a transformer depuis pandas to geopandas avant utiliser 
geometry = gpd.points_from_xy(data['lon'], data['lat'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)
#Ici on essai de faire les symbole proportionnel 
#initial view  position  , zoom et inclinaison ça sera benifique en 3D 
#choisir le jour
day = st.sidebar.slider('witch day', 0, 4, 2)
#choisir l'attribut
option = st.sidebar.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'Vent','pression','cloud'))
#construction des attribut depuis select and slider 
d=""

def att(value):
    if value== 'temperature':
        d="temp_"
    elif value== 'humidite':
        d="humdi_"
    elif value== 'vent':
        d="wind_"
    elif value== 'pression':
        d="pr_"
    elif value== 'cloud':
        d="cl_"
    return d 


   



st.pydeck_chart(pdk.Deck(
    
    initial_view_state=pdk.ViewState(
        latitude=(33),
        longitude=(-5),
        zoom=10,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=gdf,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=10,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position='[lon, lat]',
            get_radius=200,
            get_fill_color='[255,0,0]',  # Use the new 'fill_color' column
            auto_highlight=True,
           
            
           

        ),
    ]
,map_provider="mapbox",
map_style=pdk.map_styles.DARK,


))

# layer = ScatterplotLayer.from_geopandas(gdf)
# map_ = Map(layers=[layer])
# folium_static(map_)


    





