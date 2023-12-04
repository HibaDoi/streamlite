import geopandas as gpd
import streamlit as st 
from ipyleaflet import Map
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
st.set_page_config(
    page_title="Slider",
    page_icon="🗺️",
)

day = st.slider('witch day', 0, 6, 2,key='a')
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


m = leafmap.Map(height=600, center=[33, -5], zoom=12)
url = "{}cp.tif".format(str(att(option))+str(day))


m.add_raster(url, palette='viridis')

folium_static(m)



