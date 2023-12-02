import streamlit as st
from streamlit_folium import folium_static
from urllib.error import URLError
import pandas as pd
import geopandas as gpd
import leafmap
from streamlit_folium import st_folium
import pydeck as pdk



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

