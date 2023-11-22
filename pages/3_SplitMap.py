from streamlit_folium import folium_static
import leafmap.foliumap as leafmap

m = leafmap.Map(height=600, center=[33, -5], zoom=12)
url = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp0_COG.tif'
url2 = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp1_COG.tif'

m.split_map(url, url2)
m
folium_static(m)