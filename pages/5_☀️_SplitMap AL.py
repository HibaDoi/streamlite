from streamlit_folium import folium_static
import leafmap.foliumap as leafmap
import streamlit as st
# m = leafmap.Map(height=600, center=[33, -5], zoom=12)
# url = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp0_COG.tif'
# url2 = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp1_COG.tif'

# m.split_map(url, url2)


#choisir l'attribut
option = st.sidebar.selectbox(
    'Attribut',
    ('temperature', 'humidite', 'precipitation'))
# folium_static(m)
day1 = st.sidebar.slider('Left', 0, 6, 2,key="a")
day2 = st.sidebar.slider('Right', 0, 6, 3,key="b")


m = leafmap.Map(height=600, center=[33, -5], zoom=12)


def att(value):
    if value== 'temperature':
        d="temp_j"
    if value== 'humidite':
        d="humd_"
    if value== 'precipitation':
        d="preci_"
    return d 
de1=att(option)+str(day1)
de2=att(option)+str(day2)
url1 = "{}cp.tif".format(de1)
url2 = "{}cp.tif".format(de2)
m.split_map(url1,url2,
            left_args={'palette':'RdYlGn_r'}, 
            right_args={'palette':'RdYlGn'})
folium_static(m)