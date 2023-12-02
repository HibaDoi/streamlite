import streamlit as st
import pandas as pd 
import pydeck as pdk
import geopandas as gpd
import ipywidgets
#on ajoute notre fichier geoparquet
datafile ='waaaa.geoparquet'
#on lit notre fichier geoparquet
data = pd.read_parquet(datafile)
#add raw data table
if st.checkbox('show raw data'):
    st.subheader('raw data')
    st.write(data)
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)
######################################################################
isochrone_boundaries = pdk.Layer(
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
            get_fill_color='[255,6,2]', 
            auto_highlight=True,
        ),
deck=pdk.Deck(
    isochrone_boundaries,
    initial_view_state=pdk.ViewState(
        latitude=32,
        longitude=-5,
        zoom=8,
        pitch=0,
    ),
)

text = ipywidgets.HTML('heyyyyyyyy')
# def update_isochrone(widget_instance, payload):
#     text.value = "hello Word"
#     print("frfrfr")
def update_isochrone():
    text.value = "hello Word"
    
    print('trtrtr')
    
deck.deck_widget.on_click(update_isochrone)
st.pydeck_chart(deck)
st.write(text)

