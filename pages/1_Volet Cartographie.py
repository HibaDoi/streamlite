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

st.set_page_config(
    page_title="Volet Cartographie",
    page_icon="🗺️",
)
st.selectbox(    'Quelle type de symbologie?',
    ('color', 'autre'))

#on ajoute notre fichier geoparquet
datafile ='waaaa.geoparquet'
#on lit notre fichier geoparquet
data = pd.read_parquet(datafile)
#on ajoute un titre a notre page
st.header("station de meteo")
#add raw data table
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
#choisir le jour
day = st.sidebar.slider('witch day', 0, 6, 2)
#choisir l'attribut
option = st.sidebar.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'precipitation'))
#construction des attribut depuis select and slider 
d=""
def att(value):
    if value== 'temperature':
        d="temp_j"
    if value== 'humidite':
        d="humd_"
    if value== 'precipitation':
        d="preci_"
    return d 

color1 = []
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







selected_column1 = st.selectbox("Select Attribute Column:", attribute_data1)
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
st.line_chart(chart_data)

#essai nizar
#################
# la map
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
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position='[longitude, latitude]',
            get_radius=200,
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
   

# map_provider ='Google_Maps',
# api_keys="https://maps.googleapis.com/maps/api/js?key=AIzaSyBgZZK8umUqJn8d5CoIZqWPJ_qtMfqD9q0&callback=initMap&region=MA",
# map_provider='google_maps',
# map_style= None,

}
,map_provider="mapbox",
map_style=pdk.map_styles.DARK,


))

############""
deck=pdk.Deck(
    
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
            auto_highlight=True,
           
            
           

        ),
    ], 
    tooltip = {
   "html": "<b>Elevation Value:</b> {Nom_Commun} /n{OBJECTID} ",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
   
}
, 
map_provider ='Google_Maps',
map_style= 'satellite'
)
import ipywidgets
text = ipywidgets.HTML('Click near Berlin in the visualization to draw an isochrone')
def update_isochrone(widget_instance, payload):
    global deck
    global gdf
    global text

    try:
        hiba = payload['data']['index']
        
        text.value = '%s points within twenty minutes of clicked point (%s sec)' % (hiba )
        deck.update()
    except Exception as e:
        text.value = str(e)


deck.deck_widget.on_click(update_isochrone)


###############
# #for static point
# ####################*
# # Create an empty DataFrame
# ddf = pd.DataFrame()

# # Add columns to the DataFrame
# ddf['jours'] = [0,1,2,3,4,5,6] # You can replace None with any default value you want

# # Add more columns as needed

# for nh in ["temp_j","preci_","humd_"]:
#         ddf[nh] = None
# for i in range(7):
#     for nh in ["temp_j","preci_","humd_"]:
#         ddf[nh][i] = gdf.at[0, nh+str(i)]
# # Print the empty DataFrame

# chart_data = pd.DataFrame(ddf, columns=[str(att(option))])

# st.line_chart(chart_data)
##############

#chat avec un point selectionner par la list deroulante 
attribute_data= [(nom_commun, id) for nom_commun, id in zip(gdf["Nom_Commun"], gdf["OBJECTID"])]
selected_column = st.selectbox("Select Attribute Column:", attribute_data)
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
        ddf[nh][i] = gdf.at[selected_column[1], nh+str(i)]
# Print the empty DataFrame

chart_data = pd.DataFrame(ddf, columns=[str(att(option))])
#old way
# st.line_chart(chart_data)

#essai nizar
#################
import plotly.graph_objects as go

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
st.plotly_chart(fig)
##################



# # Load the TIFF files
# tif_path1 = 'temp0.tif'
# tif_path2 = 'temp1.tif'

# tif_img1 = Image.open(tif_path1)
# tif_img2 = Image.open(tif_path2)

# # Convert TIFF to numpy array
# tif_array1 = np.array(tif_img1)
# tif_array2 = np.array(tif_img2)

# # Convert numpy array to grayscale image
# tif_gray1 = Image.fromarray(tif_array1)
# tif_gray2 = Image.fromarray(tif_array2)

# # Save the grayscale images as PNG (or any other format that Folium supports)
# png_path1 = 'file1.png'
# png_path2 = 'file2.png'
# tif_gray1.save(png_path1)
# tif_gray2.save(png_path2)

# # Create a dual map
# m = plugins.DualMap(location=[33.976608456383175, -6.866780573957727], zoom_start=16)

# # Add the PNG image overlays to the map
# folium.raster_layers.ImageOverlay(
#     image=png_path1,
#     bounds=[[33.976608456383175, -6.866780573957727], [34.976608456383175, -5.866780573957727]],
#     name='Image 1',
#     show=True,
#     control=True,
#     layer_id=1,
#     interactive=True,
#     zindex=1
# ).add_to(m.m1)  # Add to the first panel

# folium.raster_layers.ImageOverlay(
#     image=png_path2,
#     bounds=[[33.976608456383175, -6.866780573957727], [34.976608456383175, -5.866780573957727]],
#     name='Image 2',
#     show=True,
#     control=True,
#     layer_id=2,
#     interactive=True,
#     zindex=1
# ).add_to(m.m2)  # Add to the second panel

# # Display the map in the Streamlit app
# folium_static(m)"""

##################
# here we do 3d representation of data with the same color
view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)
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
))

# i discovred that grid just count the number if point in one place in is nit very useful in our case 

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
))

################################################"
# view = pdk.data_utils.compute_view(df[["lng", "lat"]])
view.pitch = 75
view.bearing = 60



r = pdk.Deck(
    pdk.Layer(
    "ColumnLayer",
    data=gdf,
    get_position=["longitude", "latitude"],
    get_elevation="temp_j0",
    elevation_scale=1000,
    radius=5000,
    get_fill_color='["temp_j0"*20, "temp_j0", 234]',
    pickable=True,
    auto_highlight=True,
)
,
    initial_view_state=pdk.ViewState(
        latitude=32,
        longitude=-5,
        zoom=11,
        pitch=45,
        bearing=0,
        

    ),
    map_provider="mapbox",
    map_style=pdk.map_styles.DARK,
)
st.pydeck_chart(r)