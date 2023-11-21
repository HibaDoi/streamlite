import streamlit as st
import folium
from streamlit_folium import folium_static
import pandas as pd
import geopandas as gpd
from shapely.wkb import loads
import matplotlib.pyplot as plt
import branca
import base64
from io import BytesIO

def load_data(file_path):
    # Load data from Parquet file
    df = pd.read_parquet(file_path, engine='fastparquet')

    # Convert bytes to GeoPandas objects
    df['geometry'] = df['geometry'].apply(lambda x: loads(x))
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    return gdf

def plot_to_html(plt):
    # Convert a Matplotlib plot to HTML
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    b64 = base64.b64encode(buf.read()).decode()
    buf.close()
    return f'<img src="data:image/png;base64,{b64}" style="display:block; margin:auto;">'

def main():
    st.title("Application avec Carte de Base")

    # Load the data
    gdf = load_data('waaaa.geoparquet')

    # Create a base map centered on a specific position
    carte = folium.Map(location=[33.379103, -6.430229], zoom_start=6)

    # Add markers to the map
    for index, row in gdf.iterrows():
        try:
            latitude, longitude = row['geometry'].y, row['geometry'].x

            # Create a Matplotlib plot
            plt.figure(figsize=(6, 4))
            plt.plot(['temp_j0', 'temp_j1'], [row['temp_j0'], row['temp_j1']])
            plt.title('Temperature over Time')
            plt.xlabel('Time')
            plt.ylabel('Temperature')

            # Convert the Matplotlib plot to HTML
            html = plot_to_html(plt)

            # Create a popup with the HTML content
            popup = folium.Popup(branca.element.Html(html, script=True), max_width=2650)

            # Add a marker with the popup to the map
            folium.Marker([latitude, longitude], popup=popup).add_to(carte)

        except Exception as e:
            st.warning(f"Error extracting coordinates for point {index}: {e}")

    # Display the map in Streamlit
    folium_static(carte)

if __name__ == "__main__":
    main()