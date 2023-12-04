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
import plotly.graph_objects as go

st.set_page_config(
    page_title="Cartographie réel",
    page_icon="🗺️",
)
co1,co2=st.columns([0.5,0.5])
def bm(genre):
    if genre=="LIGHT":
        y=pdk.map_styles.LIGHT
    elif genre=="DARK":
        y=pdk.map_styles.DARK
    elif genre=="SATELLITE":
        y=pdk.map_styles.SATELLITE
    elif genre=="ROAD":
        y=pdk.map_styles.ROAD
    return y
p=co2.selectbox(    'Quelle type de symbologie vous aimez?',
    ('Variable couleur', 'Symbole Proportionnel',"3D","agg"))
#on ajoute notre fichier geoparquet
datafile ='complet.geoparquet'
#on lit notre fichier geoparquet
data = pd.read_parquet(datafile)
#on ajoute un titre a notre page
#add raw data table

if st.checkbox('show raw data'):
    st.subheader('raw data')
    st.write(data)
geometry = gpd.points_from_xy(data['lon'], data['lat'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)
day = st.sidebar.slider('witch day', 0, 4, 2)
option = st.sidebar.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'Vent','pression','cloud'))
genre = st.sidebar.radio(
    "BaseMap",
    ["LIGHT", "DARK", "SATELLITE","ROAD"])
y=bm(genre)
d=""

def att(value):
    if value== 'temperature':
        d="temp_"
    elif value== 'humidite':
        d="hmudi_"
    elif value== 'vent':
        d="wind_"
    elif value== 'pression':
        d="pr_"
    elif value== 'cloud':
        d="cl_"
    return d 
if option != 'cloud':
    gdf['cut_jenksv2'] = pd.cut(
        gdf[str(att(option))+str(day)],
                            bins=5,
                            labels=['bucket_1', 'bucket_2','bucket_3', 'bucket_4','bucket_5'],
                            include_lowest=True)
    print(gdf['cut_jenksv2'])
else:
    gdf['cut_jenksv2'] =gdf[str(att(option))+str(day)]

def cl(v):
    if option != 'cloud':
        if v=='bucket_1':
            return [0, 32, 77]
        elif v=='bucket_2':
            return [162, 38, 75]
        elif v=='bucket_3':
            return [125, 124, 120]
        elif v=='bucket_4':
            return [190, 175, 111]
        else:
            return [255, 234, 70] 
    else :
        if v == "broken clouds":
            return [249,65,68]
        elif v == "clear sky":
            return [243,114,44] 
        elif v == "few clouds":
            return [248,150,30] 
        elif v == "light rain":
            return [249,199,79] 
        elif v == "moderate rain":
            return [144,190,109] 
        elif v == "overcast clouds":
            return [67,170,139] 
        elif v == "scattered clouds":
            return [87,117,144] 
        
gdf['cut_jenksv2'] = gdf['cut_jenksv2'].astype(str)
#fonction qui fait selon les colours
def color(value):
    if att(option)== "temp_" :
        if value < 9.765:
            return [0, 32, 77]  # Red
        elif 9.765 <= value < 12.596:
            return [162, 38, 75]  # Purple
        elif 12.596 <= value < 14.637:
            return [125, 124, 120]  # Blue
        elif 14.637 <= value < 16.8:
            return [190, 175, 111]  #
        elif 16.8 <= value < 25:
            return [255, 234, 70]  #
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

gdf['fill_color1'] = gdf['cut_jenksv2'].apply(cl)


attribute_data1= [(nom_commun) for nom_commun in gdf["city_name"]]
selected_column1 = co1.selectbox("Select Attribute Column:", attribute_data1)
st.write(selected_column1)
col1, col2 = st.columns([0.5,0.5])


if selected_column1 in gdf["city_name"].values:
    # Trouvez l'index de la valeur dans la colonne A
    index_de_la_valeur = gdf.index[gdf["city_name"] == selected_column1].tolist()
    index_de_la_valeur=index_de_la_valeur[0]
st.write(index_de_la_valeur)
###################

# Create an empty DataFrame
ddf = pd.DataFrame()
ddf['jours'] = [0,1,2,3,4] # You can replace None with any default value you want
for nh in ["temp_","pr_","wind_","hmudi_"]:
        ddf[nh] = None
for i in range(5):
    for nh in ["temp_","pr_","wind_","hmudi_"]:
        ddf[nh][i] = gdf.at[index_de_la_valeur, nh+str(i)]
# Print the empty DataFrame
if option != "cloud":
    chart_data = pd.DataFrame(ddf, columns=[str(att(option))])
    #old way
    # Data
    jours=ddf['jours'] 
    temp =ddf[str(att(option))]
    # Create traces
    trace0 = go.Scatter(
        x = jours,
        y = temp,
        mode = 'lines+markers',
        name = 'temp',
        marker = dict(symbol = 'square')
    )


    data = [trace0]

    # Layout
    layout = go.Layout(
        title = 'Monthly Average Temperature',
        xaxis = dict(title = 'Months of the year'),
        yaxis = dict(title = 'Temperature (°C)'),
    )

    # Create figure
    fig = go.Figure(data=data, layout=layout)

    # Show the plot
    col2.plotly_chart(fig,use_container_width=True)
##################
genre = st.sidebar.radio(
    "Comment chercher",
    [ "nom city","coordonnée"],
    captions = [ "Chercher par la commune","Chercher par les coordonnées"])
if genre=="coordonnée":
    t=st.sidebar.text_input(
        "lat;lon",
        "33;-5",
        key="pla",
    )
    r=t.split(";")
    latt,lonn=float(r[0]),float(r[1])

if genre=="nom city":
    latt=gdf["lat"][index_de_la_valeur]
    lonn=gdf["lon"][index_de_la_valeur]
    z=10
##################
if p=='Variable couleur':
        col1.pydeck_chart(pdk.Deck(
            
            initial_view_state=pdk.ViewState(
                latitude=latt,
                longitude=lonn,
                zoom=10,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=gdf,
                    pickable=True,
                    opacity=0.8,
                    filled=True,
                    radius_scale=10,
                    radius_min_pixels=1,
                    radius_max_pixels=100,
                    line_width_min_pixels=1,
                    get_position='[lon, lat]',
                    get_radius=400,
                    get_fill_color='fill_color1',  # Use the new 'fill_color' column
                    auto_highlight=True,
                ),

                              

            ], 
            tooltip = {
        "html": "<b>Nom commune:</b> "         "  {city_name} " "      \n   "" {cl_0}  ",
        "style": {
                "backgroundColor": "steelblue",
                "color": "white"
        },
        
        }
        ,map_provider="mapbox",
        map_style=y,
        ))




    





