import streamlit as st
import folium
from streamlit_folium import folium_static
from urllib.error import URLError
import pandas as pd
import geopandas as gpd
from shapely.wkb import loads





st.set_page_config(
    page_title="Filtrage",
    page_icon="🗺️",
)

def load_hotel_data(file_path, min_lat, max_lat, min_lon, max_lon):
    # Load hotel data from Parquet file
    df = pd.read_parquet(file_path, engine='fastparquet')

    # Convert bytes to GeoPandas objects
    df['geometry'] = df['geometry'].apply(lambda x: loads(x))
    gdf = gpd.GeoDataFrame(df, geometry='geometry')

    # Filter data based on specified coordinates
    filtered_gdf = gdf.cx[min_lon:max_lon, min_lat:max_lat]

    return filtered_gdf

def add_hotel_markers(carte, gdf):
    # Add hotel markers to the map
    for index, row in gdf.iterrows():
        try:
            latitude, longitude = row['geometry'].y, row['geometry'].x

            folium.CircleMarker(
                location=[latitude, longitude],
                radius=5,
                color='blue',
                fill=True,
                fill_color='blue',
               
            ).add_to(carte)

        except Exception as e:
            st.warning(f"Error extracting coordinates for hotel {row['Hotel name']}: {e}")

def main():
    st.title("Application avec Carte de Base")

    # Create a single column for all inputs
    col1 = st.sidebar

    # User input for filtering coordinates
    st.sidebar.subheader("Filter Coordinates")
    min_latitude = st.sidebar.number_input("Enter Minimum Latitude:", value=-90.0, min_value=-90.0, max_value=90.0)
    max_latitude = st.sidebar.number_input("Enter Maximum Latitude:", value=90.0, min_value=-90.0, max_value=90.0)
    min_longitude = st.sidebar.number_input("Enter Minimum Longitude:", value=-180.0, min_value=-180.0, max_value=180.0)
    max_longitude = st.sidebar.number_input("Enter Maximum Longitude:", value=180.0, min_value=-180.0, max_value=180.0)

    # Create a base map centered on a specific position
    carte = folium.Map(location=[33.379103, -6.430229], zoom_start=6)

    try:
        # Load all data to get column names for the attribute selection
        gdf_all = load_hotel_data(r"waaaa.geoparquet",
                                  min_latitude, max_latitude, min_longitude, max_longitude)

        # Exclude specific columns from the attribute selection, including "geometry"
        excluded_columns = ["FID","OBJECTID","Code_Commu","Nom_Commun","Nom_Comm_1","Code_Provi","CODE_REGIO","Code_Com_O","Nom_Com_Ol","Shape__Are","Shape__Len","Shape__A_1","Shape__L_1","ORIG_FID","latitude","longitude","OBJECTID_1","Type_Commu"]
        attribute_columns = [col for col in gdf_all.columns if col not in excluded_columns]

        # Get user input for selecting attribute column
        selected_column = st.sidebar.selectbox("Select Attribute Column:", attribute_columns)

        # Get user input for filtering column values
        min_value = st.sidebar.number_input(f"Enter Minimum Value for {selected_column}:", value=gdf_all[selected_column].min())
        max_value = st.sidebar.number_input(f"Enter Maximum Value for {selected_column}:", value=gdf_all[selected_column].max())

        # Load filtered hotel data based on both attribute column values and spatial coordinates
        gdf_filtered = gdf_all[(gdf_all[selected_column] >= min_value) & (gdf_all[selected_column] <= max_value)]

        # Add hotel markers to the map
        add_hotel_markers(carte, gdf_filtered)

        # Display the updated map in Streamlit
        folium_static(carte)

    except URLError as e:
        st.error(f"URL Error: {e}")

    except Exception as e:
        st.error(f"Error: {e}")

if __name__ == "__main__":
    main()