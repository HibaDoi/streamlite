import streamlit as st
import pandas as pd 
import numpy as np
import pydeck as pdk
import geopandas as gpd
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

color1 = []

def color(value):
    if value < 15:
        return [246, 45, 45]  # Red
    elif 15 <= value < 35:
        return [162, 38, 75]  # Purple
    else:
        return [16, 52, 166]  # Blue



d=""
def att(value):
    if value== 'temperature':
        d="temp_j"
    if value== 'humidite':
        d="humd_"
    if value== 'precipitation':
        d="preci_"
    return d 

gdf['fill_color'] = gdf[str(att(option))+str(day)].apply(color)



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
        ),
    ],
))
# here we do 3d representation of data with the same color
"""view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)
st.pydeck_chart(pdk.Deck(
    views=[view],
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=32,
        longitude=-5,
        zoom=5,
        pitch=0,
    ),
    parameters={"cull": True},
    #Ici on peut ajouter une infinitée de couche et ler symbology 
    layers=[
    pdk.Layer(
        "ColumnLayer",
        id="temp_j3",
        data=gdf,
        get_elevation="temp_j3",
        get_position=["longitude", "latitude"],
        elevation_scale=1000,
        pickable=True,
        auto_highlight=True,
        radius=2000,
        get_fill_color='[255, 165, 0]',
        ),
        
    ],
))"""

# i discovred that grid just count the number if point in one place in is nit very useful in our case 
"""
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=32,
        longitude=-5,
        zoom=11,
        pitch=45,
        bearing=0,
        

    ),
    #Ici on peut ajouter une infinitée de couche et ler symbology 
    layers=[
       pdk.Layer(
    "GridLayer",
    gdf,
    pickable=True,
    extruded=True,
    cell_size=20000,
    elevation_scale=5,
    get_position=["longitude", "latitude"],
)
        
    ],
))"""