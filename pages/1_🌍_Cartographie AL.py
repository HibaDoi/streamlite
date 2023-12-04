import streamlit as st
import pandas as pd 
import pydeck as pdk
import geopandas as gpd
import plotly.graph_objects as go
from localtileserver.widgets import get_folium_tile_layer
import streamlit as st
from streamlit_folium import folium_static
import numpy as np
from rasterio.warp import transform_bounds

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
st.set_page_config(
    page_title="Cartographier",
    page_icon="🗺️",
)

p=st.sidebar.selectbox(    'Quelle type de symbologie vous aimez?',
    ('Variable couleur', 'Symbole Proportionnel',"3D","Grid"))
#on ajoute notre fichier geoparquet
datafile ='waaaa.geoparquet'
#on lit notre fichier geoparquet
data = pd.read_parquet(datafile)
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)
#Ici on essai de faire les symbole proportionnel 
#initial view  position  , zoom et inclinaison ça sera benifique en 3D 
#choisir le jour
if st.checkbox('show raw data'):
    st.subheader('raw data')
    st.write(data)

day = st.sidebar.slider('witch day', 0, 6, 2)
#choisir l'attribut
option = st.sidebar.selectbox(
    'Choisit attribut ',
    ('temperature', 'humidite', 'precipitation'))
genre = st.sidebar.radio(
    "BaseMap",
    ["LIGHT", "DARK", "SATELLITE","ROAD"])
y=bm(genre)
def att(value):
    if value== 'temperature':
        d="temp_j"
    if value== 'humidite':
        d="humd_"
    if value== 'precipitation':
        d="preci_"
    return d 

#fonction qui fait selon les colours
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
attribute_data1= [(nom_commun) for nom_commun in gdf["Nom_Commun"]]
col1, col2 = st.columns([0.3, 0.7])
selected_column1 = col1.selectbox("Select Attribute Column:", attribute_data1)
st.write(selected_column1)

if selected_column1 in gdf["Nom_Commun"].values:
    # Trouvez l'index de la valeur dans la colonne A
    index_de_la_valeur = gdf.index[gdf["Nom_Commun"] == selected_column1].tolist()
    index_de_la_valeur=index_de_la_valeur[0]
st.write(index_de_la_valeur)
###################

# Create an empty DataFrame
ddf = pd.DataFrame()

# Add columns to the DataFrame
ddf['jours'] = [0,1,2,3,4,5,6] # You can replace None with any default value you want

# Add more columns as needed

for nh in ["temp_j","preci_","humd_"]:
        ddf[nh] = None
for i in range(7):
    for nh in ["temp_j","preci_","humd_"]:
        ddf[nh][i] = gdf.at[index_de_la_valeur, nh+str(i)]
# Print the empty DataFrame

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
    
    xaxis = dict(title = 'Days'),
    yaxis = dict(title = str(att(option))+str(day)),
)

# Create figure
fig = go.Figure(data=data, layout=layout)

# Show the plot
col2.plotly_chart(fig,use_container_width=True)
##################
if p=='Variable couleur':
        st.pydeck_chart(pdk.Deck(
            
            initial_view_state=pdk.ViewState(
                latitude=(gdf["latitude"][index_de_la_valeur]),
                longitude=(gdf["longitude"][index_de_la_valeur]),
                zoom=5,
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
                    get_position='[longitude, latitude]',
                    get_radius=400,
                    get_fill_color='fill_color',  # Use the new 'fill_color' column
                    auto_highlight=True,
                
                    
                

                ),
            ], 
            tooltip = {
        "html": "<b>Nom commune:</b> "         "  {Nom_Commun} \n {OBJECTID} ",
        "style": {
                "backgroundColor": "steelblue",
                "color": "white"
        },
        
        }
        ,map_provider="mapbox",
        map_style=y,


        ))
elif p=='Symbole Proportionnel':
        st.pydeck_chart(pdk.Deck(
            
            initial_view_state=pdk.ViewState(
                latitude=(gdf["latitude"][index_de_la_valeur]),
                longitude=(gdf["longitude"][index_de_la_valeur]),
                zoom=10,
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
                    radius_max_pixels=500,
                    line_width_min_pixels=1,
                    get_position='[longitude, latitude]',
                    get_radius=str(att(option))+str(day),
                    get_fill_color='[255,0,0]',  # Use the new 'fill_color' column
                    auto_highlight=True,
 
            ),
        ], 
        tooltip = {
    "html": "<b>Nom commune:</b> "         "  {Nom_Commun} \n {OBJECTID} ",
    "style": {
            "backgroundColor": "steelblue",
            "color": "white"
    },
        }
        
        ,map_provider="mapbox",
        map_style=y,))
elif p=='3D':
        # here we do 3d representation of data with the same color
    view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)
    st.pydeck_chart(pdk.Deck(
        views=[view],
        
        initial_view_state=pdk.ViewState(
            latitude=32,
            longitude=-5,
            zoom=6,
            pitch=45,
        ),
        parameters={"cull": True},
        #Ici on peut ajouter une infinitée de couche et ler symbology 
        layers=[
        pdk.Layer(
            "ColumnLayer",
            id="OBJECTID",
            data=gdf,
            get_elevation=(str(att(option))+str(day)),
            get_position=["longitude", "latitude"],
            elevation_scale=1000,
            pickable=True,
            auto_highlight=True,
            radius=2000,
            get_fill_color='[255, 165, 0]',
            ),
            
        ],
        map_provider="mapbox",
        map_style=y,
    ))
elif p=="Grid":
    st.pydeck_chart(pdk.Deck(
    
    initial_view_state=pdk.ViewState(
        latitude=32,
        longitude=-5,
        zoom=5,
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
     map_provider="mapbox",
        map_style=y,
))