import streamlit as st
import folium
from streamlit_folium import folium_static
from urllib.error import URLError
import pandas as pd
import geopandas as gpd
from shapely.wkb import loads

def main():
    # Titre de l'application
    st.title("Application avec Carte de Base")

    # Création d'une carte de base centrée sur une position spécifique
    carte = folium.Map(location=[33.379103, -6.430229], zoom_start=6)

    # Ajout d'un marqueur sur la carte
    # folium.Marker([33.985135, -6.858640], popup="Rabat").add_to(carte)

    # Ajouter une zone de texte pour les coordonnées
    coords_input = st.text_input("Entrez les coordonnées (format : latitude, longitude):")

    # Ajouter un bouton de recherche
    if st.button("Rechercher"):
        try:
            # Effacer tous les marqueurs existants
            # for layer in carte._children:
            #     # if isinstance(layer, folium.Marker):
            #     #     layer.add_to(carte)

            # Vérifier si des coordonnées ont été entrées
            if coords_input:
                # Extraire les coordonnées à partir de la zone de texte
                entered_latitude, entered_longitude = map(float, coords_input.split(','))

                # # Charger le fichier Parquet avec pandas et fastparquet
                # df = pd.read_parquet("waaaa.geoparquet")

                # # Convertir les objets bytes en objets GeoPandas
                # df['geometry'] = df['geometry'].apply(lambda x: loads(x))
                # gdf = gpd.GeoDataFrame(df, geometry='geometry')

                # # Ajouter un seul marqueur pour les coordonnées entrées en rouge
                # for index, row in gdf.iterrows():
                #     try:
                #         # Extraire les coordonnées à partir de la colonne 'geometry'
                #         latitude, longitude = row['geometry'].y, row['geometry'].x

                #         if latitude == entered_latitude and longitude == entered_longitude:
                #             folium.Marker(
                #                 location=[latitude, longitude],
                            
                #                 icon=folium.Icon(color='red')
                #             ).add_to(carte)

                #     except Exception as e:
                #         st.warning(f"Erreur lors de l'extraction des coordonnées pour l'hôtel {row['Hotel name']} : {e}")

                # # Ajouter les points du GeoDataFrame à la carte folium (en bleu)
                # for index, row in gdf.iterrows():
                #     try:
                #         # Extraire les coordonnées à partir de la colonne 'geometry'
                #         latitude, longitude = row['geometry'].y, row['geometry'].x

                #         folium.CircleMarker(
                #             location=[latitude, longitude],
                #             radius=5,
                #             color='blue',
                #             fill=True,
                #             fill_color='blue',
                            
                #         ).add_to(carte)

                #     except Exception as e:
                #         st.warning(f"Erreur lors de l'extraction des coordonnées pour l'hôtel {row['Hotel name']} : {e}")

                # Afficher la carte mise à jour dans Streamlit
                folium_static(carte)

        except URLError as e:
            # Gestion des erreurs liées aux URL
            st.error(f"Erreur d'URL : {e}")

        except Exception as e:
            # Gestion générique des erreurs
            st.error(f"Erreur : {e}")

if __name__ == "__main__":
    main()