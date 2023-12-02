from streamlit_folium import folium_static
import leafmap.foliumap as leafmap
import streamlit as st
# m = leafmap.Map(height=600, center=[33, -5], zoom=12)
# url = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp0_COG.tif'
# url2 = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp1_COG.tif'

# m.split_map(url, url2)
# m

#choisir l'attribut
option = st.sidebar.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'pression','vent'))
# folium_static(m)
day1 = st.sidebar.slider('witch day', 0, 6, 2,key="a")
day2 = st.sidebar.slider('witch day', 0, 6, 2,key="b")
m = leafmap.Map(height=600, center=[33, -5], zoom=12)
url = 'Idw_POWER_Re11.tif'
url2 = 'Idw_POWER_Re11.tif'

m.split_map(url, url2)
m
folium_static(m)