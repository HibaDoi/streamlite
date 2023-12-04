import streamlit as st
from streamlit_folium import folium_static
from urllib.error import URLError
import pandas as pd
import geopandas as gpd
import leafmap
from streamlit_folium import st_folium
import pydeck as pdk

###################################
def att(value):
    d=""
    if value== 'temperature':
        d="temp_j"
    if value== 'humidite':
        d="humd_"
    if value== 'precipitation':
        d="preci_"
    return d 
def color(value,option):
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
def cho(value,cool):
    if value== 'temperature':
        slider_range=cool.slider("Values",0,50,value=[0,50],key="slider_key1"+str(cool))
    if value== 'humidite':
        slider_range=cool.slider("Values",0,100,value=[0,100],key="slider_key2"+str(cool))
    if value== 'precipitation':
        slider_range=cool.slider("Values",0,20 ,value=[0,20],key="slider_key3"+str(cool))
    return slider_range
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
def hextorgb(hex_color):
    # Remove '#' if present
    hex_color = hex_color.lstrip('#')
    
    # Extract RGB components
    red = int(hex_color[0:2], 16)
    green = int(hex_color[2:4], 16)
    blue = int(hex_color[4:6], 16)
    
    return red, green, blue



####################################################################
st.set_page_config(page_title="Requête",page_icon="🗺️",)
genre = st.sidebar.radio(
    "BaseMap",
    ["LIGHT", "DARK", "SATELLITE","ROAD"])
y=bm(genre)
datafile ='waaaa.geoparquet'
data = pd.read_parquet(datafile)
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)
###############
rlong=st.sidebar.slider("Longitude",-180,180 ,value=[-180,180],key="h")
rlat=st.sidebar.slider("Latitude",-90,90 ,value=[-90,90],key="n")
###############
col1, col2 ,col3= st.columns(3)
#col1
day = col1.slider('witch day', 0, 6, 2,key="slider_key4")
#col2
option = col2.selectbox('How would you like to choose?',
    ('temperature', 'humidite', 'precipitation'),key="select_box2")
#col3
s=cho(option,col3)
##############
r=att(option)
t=str(r)+str(day)

fil_gdf1 = gdf[(gdf[t] >= s[0]) & (gdf[t] <= s[1])]
##############
fil_gdf = fil_gdf1.cx[rlong[0]:rlong[1], rlat[0]:rlat[1]]
print(fil_gdf1)

print(fil_gdf1)
###########
col7,col8,col9=st.columns(3)

def rui(res,fil_gdf):
    if res:
        option1 = col8.selectbox('How would you like to chooseee?',
        ('temperature', 'humidite', 'precipitation'),key="select_box4554")
        s1=cho(option1,col9)
        r1=att(option1)
        t1=str(r1)+str(day)
        fil_gdf = fil_gdf[(fil_gdf[t1] >= s1[0]) & (fil_gdf[t1] <= s1[1])]
        return fil_gdf

col10,col11,col12=st.columns(3)
def ruiI(res,fil_gdf):
    if res:
        option2 = col11.selectbox('How would you like to cccchooseee?',
        ('temperature', 'humidite', 'precipitation'),key="select_box455334")
        s2=cho(option2,col12)
        r2=att(option2)
        t2=str(r2)+str(day)
        fil_gdf = fil_gdf[(fil_gdf[t2] >= s2[0]) & (fil_gdf[t2] <= s2[1])]
        return fil_gdf
a=col7.toggle("ADD Clause",key="hiba")
b=col10.toggle("ADD Clausee",key="safa")
print(a,b)

if a is False and b is False:
    t=fil_gdf
elif b is False :
    t=rui(a,fil_gdf) 
else:
    t=rui(a,fil_gdf) 
    t=ruiI(b,t)

###############
color = st.sidebar.color_picker('Pick A Color', '#00f900')
fil_gdf['fill_color'] = [hextorgb(color)] * len(fil_gdf)

############""
hh=pdk.ViewState(
        latitude=33,
        longitude=-5,
        zoom=5,
        pitch=0,
    )

layerss=pdk.Layer(
            'ScatterplotLayer',
            data=t,
            pickable=True,
            opacity=0.8,
            stroked=False,
            filled=True,
            radius_scale=10,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position='[longitude, latitude]',
            get_radius=300,
            get_fill_color='fill_color',  # Use the new 'fill_color' column
            auto_highlight=True, 

        )
    

st.pydeck_chart(pdk.Deck(initial_view_state=hh,layers=layerss,
    map_provider="mapbox",
    
    map_style=y, ))


