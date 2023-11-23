import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import streamlit as st 


st.set_page_config(
    page_title="Slider",
    page_icon="🗺️",
)


day = st.slider('witch day', 0, 6, 2)
option = st.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'precipitation'))

# Load your GeoDataFrame from Parquet (assuming it has geometry columns)
gdf = gpd.read_parquet('waaaa.geoparquet')

# List of attribute columns
temp_attributes = ['temp_j0', 'temp_j1', 'temp_j2','temp_j3', 'temp_j4', 'temp_j5','temp_j6']
humd_attributes = ['humd_0', 'humd_1', 'humd_2','humd_3', 'humd_4', 'humd_5', 'humd_6']
preci_attributes = ['preci_0', 'preci_1', 'preci_2','preci_3', 'preci_4', 'preci_5', 'preci_6']

d=""
def att(value):
    if value== 'temperature':
        d="temp_j"
    if value== 'humidite':
        d="humd_"
    if value== 'precipitation':
        d="preci_"
    return d 
# Define the classification bins
temp_bins = [0, 15, 30, 50]
humd_bins = [0, 20, 40, 60, 100]
preci_bins = [0, 5, 10, 15, 20]
###################""
for attribute in temp_attributes + humd_attributes + preci_attributes:
    if str(att(option))+str(day)==attribute:
         # Create a new column for the classification
        if attribute in temp_attributes:
            bins = temp_bins
        elif attribute in humd_attributes:
            bins = humd_bins
        else:  # attribute in preci_attributes
            bins = preci_bins

        gdf['class'] = pd.cut(gdf[attribute], bins, labels=False, include_lowest=True)

        # Create a new figure
        fig, ax = plt.subplots(1, 1)

        # Create the map
        gdf.plot(column='class', cmap='viridis', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

        # Remove x and y axis information
        ax.axis('off')
        ax.set_title(f'{option}   on Day {day}', fontdict={'fontsize': '15', 'fontweight' : '3'})

        # Save the figure as a PNG
        fig.savefig(f'{attribute}_map.png')
        st.image(f'{attribute}_map.png')
        ax.set_title(f'{option}   on Day {day}', fontdict={'fontsize': '15', 'fontweight' : '3', 'color': 'white'})
        st.plotly_chart(fig)


###################

def rr(h):
    a=h[:-1]
    b=h[-1]
    return a,b
t=""
def att(value):
    if value in "temp_j" :
        t='temperature'
    elif value in "humd_":
        t='humidite'
    elif value in "preci_":
        t='precipitation'
    return t

for attribute in temp_attributes + humd_attributes + preci_attributes:
    # Create a new column for the classification
    if attribute in temp_attributes:
        bins = temp_bins
    elif attribute in humd_attributes:
        bins = humd_bins
    else:  # attribute in preci_attributes
        bins = preci_bins
    uu=rr(attribute)[0]
    oo=rr(attribute)[1]
   
    nh=att(uu)
   

    gdf['class'] = pd.cut(gdf[attribute], bins, labels=False, include_lowest=True)

    # Create a new figure
    fig, ax = plt.subplots(1, 1)

    # Create the map
    gdf.plot(column='class', cmap='viridis', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

    # Remove x and y axis information
    ax.axis('off')
    ax.set_title(f'{nh} jour {oo}', fontdict={'fontsize': '15', 'fontweight': '3'})

    # Save the figure as a PNG
    fig.savefig(f'{attribute}_map.png')
    # st.plotly_chart(fig)