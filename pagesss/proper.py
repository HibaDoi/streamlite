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



#on ajoute notre fichier geoparquet
datafile ='waaaa.geoparquet'
#on lit notre fichier geoparquet
data = pd.read_parquet(datafile)
#on ajoute un titre a notre page
st.header("station de meteo")
#add raw data 
if st.checkbox('show raw data'):
    st.subheader('raw data')
    st.write(data)
#on affiche la map
#st.map(data)
#on affiche avec symbologie
# Ici on a trouver une erreur dans laquel on a transformer depuis pandas to geopandas avant utiliser 
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)

#Ici on essai de faire les symbole proportionnel 
#initial view  position  , zoom et inclinaison ça sera benifique en 3D 


# Assuming 'temp_j3' is a column in your GeoDataFrame




day = st.slider('witch day', 0, 6, 2)
option = st.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'precipitation'))

d=""
def att(value):
    if value== 'temperature':
        d="temp_j"
    if value== 'humidite':
        d="humd_"
    if value== 'precipitation':
        d="preci_"
    return d 
###################
def get_weather(day, value):
    if day == 0:
        if value == "temperature":
            return temp_j0
        elif value == "humidite":
            return humid_0
        elif value == "precipitation":
            return preci_0
    elif day == 1:
        if value == "temperature":
            return temp_j1
        elif value == "humidite":
            return humid_1
        elif value == "precipitation":
            return preci_1
    elif day == 2:
        if value == "temperature":
            return temp_j2
        elif value == "humidite":
            return humid_2
        elif value == "precipitation":
            return preci_2
    elif day == 3:
        if value == "temperature":
            return temp_j3
        elif value == "humidite":
            return humid_3
        elif value == "precipitation":
            return preci_3
    elif day == 4:
        if value == "temperature":
            return temp_j4
        elif value == "humidite":
            return humid_4
        elif value == "precipitation":
            return preci_4
    elif day == 5:
        if value == "temperature":
            return temp_j5
        elif value == "humidite":
            return humid_5
        elif value == "precipitation":
            return preci_5
    elif day == 6:
        if value == "temperature":
            return temp_j6
        elif value == "humidite":
            return humid_6
        elif value == "precipitation":
            return preci_6
###################




color1 = []

def color(value):
    if att(option)== "temp_j" :
        if value < 15:
            return [246, 45, 45]  # Red
        elif 15 <= value < 35:
            return [162, 38, 75]  # Purple
        else:
            return [16, 52, 166]  # Blue
    if att(option)== "humd_" :
        if value < 30:
            return [135, 97, 115]  # Red
        elif 15 <= value < 60:
            return [176, 147, 101]  # Purple
        else:
            return [20, 120, 51]  # Blue
    if att(option)== "preci_" :
        if value < 7:
            return [0, 212, 14]  # Red
        elif 15 <= value < 14:
            return [0, 113, 133]  # Purple
        else:
            return [0, 49, 147]  # Blue





gdf['fill_color'] = gdf[str(att(option))+str(day)].apply(color)

# Create a new column 'label' containing the labels for each point

def hh():
    i
hey=str(att(option))+str(day)
print(hey)
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=32,
        longitude=-5,
        zoom=8,
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
            get_position='[longitude, latitude]',
            get_radius=200,
            get_fill_color='fill_color',  # Use the new 'fill_color' column
            auto_highlight=True,
            
           

        ),
    ], 
    tooltip={"text": " {temp_j0} \n {temp_j1} \n {get_weather()}"  }
))


####################
##############

#chart
###################
# Create an empty DataFrame
ddf = pd.DataFrame()

# Add columns to the DataFrame
ddf['jours'] = [0,1 ,2,3,4,5,6] # You can replace None with any default value you want

# Add more columns as needed
ddf['temp'+str(0)] = None
for i in range(7):
    ddf['temp'+str(0)][i] = gdf.at[0, 'temp_j'+str(i)]
# Print the empty DataFrame
#print(ddf)
chart_data = pd.DataFrame(ddf, columns=["temp0"])

st.line_chart(chart_data)
##################
# m = leafmap.Map(height=600, center=[39.4948, -108.5492], zoom=12)
# url = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp0_COG.tif'
# url2 = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp1_COG.tif'
# m.split_map(url, url2)
# m
# folium_static(m)