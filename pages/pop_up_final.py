import folium
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import branca
from streamlit_folium import folium_static
import streamlit as st
from streamlit_folium import st_folium
import plotly.graph_objects as go
# Load your data
df = pd.read_parquet('waaaa.geoparquet')  # replace with your actual file path

# Create a map
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=13)




###########3
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
###########3


# Add points to the map
for idx, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']]).add_to(m)   
# Display the map
# folium_static(m)
# ff={'la'}
data=st_folium(m)
st.sidebar.write(data["last_object_clicked"])
ff=data["last_object_clicked"]
if( ff['lat'] in df["latitude"].values )& (ff['lng'] in df["longitude"].values ):
    # Trouvez l'index de la valeur dans la colonne A
    index_de_la_valeur = df.index[(df["latitude"] == ff['lat'] )& (df["longitude"]==ff['lng'] ) ].tolist()
    index_de_la_valeur=index_de_la_valeur[0]
st.write(index_de_la_valeur)

ddf = pd.DataFrame()

# Add columns to the DataFrame
ddf['jours'] = [0,1,2,3,4,5,6] # You can replace None with any default value you want

# Add more columns as needed

for nh in ["temp_j","preci_","humd_"]:
        ddf[nh] = None
for i in range(7):
    for nh in ["temp_j","preci_","humd_"]:
        ddf[nh][i] = df.at[index_de_la_valeur, nh+str(i)]
# Print the empty DataFrame

chart_data = pd.DataFrame(ddf, columns=[str(att(option))])
#old way
st.line_chart(chart_data)
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
st.plotly_chart(fig,use_container_width=True)