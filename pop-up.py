import plotly.express as px
import folium
import branca
import streamlit as st
import pandas as pd 
import geopandas as gpd
from streamlit_folium import folium_static
#on ajoute notre fichier geoparquet
datafile ='waaaa.geoparquet'
#on lit notre fichier geoparquet
data = pd.read_parquet(datafile)
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)

df = px.data.gapminder().query("country=='Canada'")
fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
fig.update_layout(margin=dict(t=30,l=10,b=10,r=10))
fig.write_html('/content/popup_map.html')

filepath = 'popup_map.html'
with open(filepath , encoding='utf-8') as f:
    html = f.read()

coor1= [19.742110608748604, -99.01751491998121]
geomap = folium.Map([19.715576, -99.20099], zoom_start=9, tiles="OpenStreetMap")

iframe = branca.element.IFrame(html=html, width=500, height=300)
popup = folium.Popup(iframe, max_width=500)

folium.Marker([coor1[0],coor1[1]], popup=popup).add_to(geomap)

geomap