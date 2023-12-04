import folium
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import branca
from streamlit_folium import folium_static
import streamlit as st
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
    # Create a plot for each point
    fig, ax = plt.subplots()
    ax.plot([att(option)+'0', att(option)+'1', att(option)+'2',att(option)+'3',att(option)+'4',att(option)+'5',att(option)+'6'], [row[att(option)+'0'], row[att(option)+'1'], row[att(option)+'2'],row[att(option)+'3'],row[att(option)+'4'],row[att(option)+'5'],row[att(option)+'6']])
    
    # Convert plot to HTML
    html = '<img src="data:image/png;base64,{}">'.format
    buf = BytesIO()
    plt.savefig(buf, format='png')  # Save the plot to the buffer before closing it
    plt.close(fig)  # Now you can close the plot
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    buf.close()
    encoded = html(b64)

    # Create a popup with the plot
    iframe = branca.element.IFrame(encoded, width=800, height=800)
    popup = folium.Popup(iframe, max_width=800)

    # Add a marker with the popup to the map
    folium.Marker([row['latitude'], row['longitude']], popup=popup).add_to(m)   


# Display the map
folium_static(m)