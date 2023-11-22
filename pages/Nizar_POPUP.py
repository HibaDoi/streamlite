import folium
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import branca

# Load your data
df = pd.read_parquet('waaaa.geoparquet')  # replace with your actual file path

# Create a map
m = folium.Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=13)

# Add points to the map
for idx, row in df.iterrows():
    # Create a plot for each point
    fig, ax = plt.subplots()
    ax.plot(['temp_j0', 'temp_j1', 'temp_j2'], [row['temp_j0'], row['temp_j1'], row['temp_j2']])
    
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
    iframe = branca.element.IFrame(encoded, width=500, height=300)
    popup = folium.Popup(iframe, max_width=500)

    # Add a marker with the popup to the map
    folium.Marker([row['latitude'], row['longitude']], popup=popup).add_to(m)
# Display the map
m
from streamlit_folium import folium_static

# Display the map
folium_static(m)