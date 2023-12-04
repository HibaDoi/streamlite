import streamlit as st 
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
st.set_page_config(
    page_title="Slider",
    page_icon="🗺️",
)

day = st.sidebar.slider('witch day', 0, 6, 2,key='a')
option = st.sidebar.selectbox(
    'Attribut',
    ('temperature', 'humidite', 'precipitation'))

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



