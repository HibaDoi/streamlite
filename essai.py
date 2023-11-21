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
############

##############
# Create a new column 'label' containing the labels for each point



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
            auto_highlight=True,
            
           

        ),
    ], 
    tooltip = {
   "html": "<b>Elevation Value:</b> {OBJECTID}",
   "style": {
        "backgroundColor": "steelblue",
        "color": "white"
   }
}
))

#fromm mappp
####################*
# Create an empty DataFrame
ddf = pd.DataFrame()

# Add columns to the DataFrame
ddf['jours'] = [0,1,2,3,4,5,6] # You can replace None with any default value you want

# Add more columns as needed

for nh in ["temp_j","preci_","humd_"]:
        ddf[nh] = None
for i in range(7):
    for nh in ["temp_j","preci_","humd_"]:
        ddf[nh][i] = gdf.at[0, nh+str(i)]
# Print the empty DataFrame
print(ddf)
chart_data = pd.DataFrame(ddf, columns=[str(att(option))])
print(chart_data)
st.line_chart(chart_data)
##############

#chart
attribute_columns = [col for col in gdf["OBJECTID"] ]
selected_column = st.selectbox("Select Attribute Column:", attribute_columns)
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
        ddf[nh][i] = gdf.at[selected_column, nh+str(i)]
# Print the empty DataFrame
print(ddf)
chart_data = pd.DataFrame(ddf, columns=[str(att(option))])
print(chart_data)
st.line_chart(chart_data)
##################
m = leafmap.Map(height=600, center=[39.4948, -108.5492], zoom=12)
url = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp0_COG.tif'
url2 = 'https://essainh1119.s3.us-east-2.amazonaws.com/webmapping/temp1_COG.tif'
m.split_map(url, url2)
m
folium_static(m)


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
# view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)
# st.pydeck_chart(pdk.Deck(
#     views=[view],
#     map_style=None,
#     initial_view_state=pdk.ViewState(
#         latitude=32,
#         longitude=-5,
#         zoom=5,
#         pitch=0,
#     ),
#     parameters={"cull": True},
#     #Ici on peut ajouter une infinitée de couche et ler symbology 
#     layers=[
#     pdk.Layer(
#         "ColumnLayer",
#         id="temp_j3",
#         data=gdf,
#         get_elevation="temp_j3",
#         get_position=["longitude", "latitude"],
#         elevation_scale=1000,
#         pickable=True,
#         auto_highlight=True,
#         radius=2000,
#         get_fill_color='[255, 165, 0]',
#         ),
        
#     ],
# ))

# i discovred that grid just count the number if point in one place in is nit very useful in our case 

# st.pydeck_chart(pdk.Deck(
#     map_style=None,
#     initial_view_state=pdk.ViewState(
#         latitude=32,
#         longitude=-5,
#         zoom=11,
#         pitch=45,
#         bearing=0,
        

#     ),
#     #Ici on peut ajouter une infinitée de couche et ler symbology 
#     layers=[
#        pdk.Layer(
#     "GridLayer",
#     gdf,
#     pickable=True,
#     extruded=True,
#     cell_size=20000,
#     elevation_scale=5,
#     get_position=["longitude", "latitude"],
# )
        
#     ],
# ))