import streamlit as st
import pandas as pd 
import pydeck as pdk
import geopandas as gpd
import streamlit as st
import plotly.graph_objects as go
st.set_page_config(
    page_title="Cartographie réel",
    page_icon="🗺️",
)
def bm(genre):
    if genre=="LIGHT":
        y=pdk.map_styles.CARTO_LIGHT_NO_LABELS
    elif genre=="DARK":
        y=pdk.map_styles.CARTO_DARK_NO_LABELS
    elif genre=="SATELLITE":
        y=pdk.map_styles.SATELLITE
    elif genre=="ROAD":
        y=pdk.map_styles.ROAD
    return y
p=st.sidebar.selectbox(    'Quelle type de symbologie vous aimez?',
    ('Variable couleur', 'Symbole Proportionnel',"3D","Grid"))
#on ajoute notre fichier geoparquet
datafile ='complet.geoparquet'
#on lit notre fichier geoparquet
data = pd.read_parquet(datafile)
#on ajoute un titre a notre page

#add raw data table
if st.checkbox('show raw data'):
    st.subheader('raw data')
    st.write(data)
#on affiche la map
#st.map(data)
#on affiche avec symbologie
# Ici on a trouver une erreur dans laquel on a transformer depuis pandas to geopandas avant utiliser 
geometry = gpd.points_from_xy(data['lon'], data['lat'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)
#Ici on essai de faire les symbole proportionnel 
#initial view  position  , zoom et inclinaison ça sera benifique en 3D 
#choisir le jour
day = st.sidebar.slider('witch day', 0, 4, 2)
#choisir l'attribut
option = st.sidebar.selectbox(
    'Choisit attribut ',
    ('temperature', 'humidite', 'Vent','pression','cloud'))
#construction des attribut depuis select and slider 
genre = st.sidebar.radio(
    "BaseMap",
    ["LIGHT", "DARK", "SATELLITE","ROAD"])
y=bm(genre)
def att(value):
    if value== 'temperature':
        d="temp_"
    elif value== 'humidite':
        d="hmudi_"
    elif value== 'vent':
        d="wind_"
    elif value== 'pression':
        d="pr_"
    elif value== 'cloud':
        d="cl_"
    return d 

#fonction qui fait selon les colours
if option != 'cloud':
    gdf['cut_jenksv2'] = pd.cut(
        gdf[str(att(option))+str(day)],
                            bins=5,
                            labels=['bucket_1', 'bucket_2','bucket_3', 'bucket_4','bucket_5'],
                            include_lowest=True)
  
else:
    gdf['cut_jenksv2'] =gdf[str(att(option))+str(day)]

def cl(v):
    if option != 'cloud':
        if v=='bucket_1':
            return [0, 32, 77]
        elif v=='bucket_2':
            return [162, 38, 75]
        elif v=='bucket_3':
            return [125, 124, 120]
        elif v=='bucket_4':
            return [190, 175, 111]
        else:
            return [255, 234, 70] 
    else :
        if v == "broken clouds":
            return [249,65,68]
        elif v == "clear sky":
            return [243,114,44] 
        elif v == "few clouds":
            return [248,150,30] 
        elif v == "light rain":
            return [249,199,79] 
        elif v == "moderate rain":
            return [144,190,109] 
        elif v == "overcast clouds":
            return [67,170,139] 
        elif v == "scattered clouds":
            return [87,117,144] 
 
gdf['cut_jenksv2'] = gdf['cut_jenksv2'].astype(str)

gdf['fill_color1'] = gdf['cut_jenksv2'].apply(cl)

attribute_data1= [(nom_commun) for nom_commun in gdf["city_name"]]

col1, col2 = st.columns([0.3, 0.7])
selected_column1 = col1.selectbox("Select Attribute Column:", attribute_data1)
st.write(selected_column1)

if selected_column1 in gdf["city_name"].values:
    # Trouvez l'index de la valeur dans la colonne A
    index_de_la_valeur = gdf.index[gdf["city_name"] == selected_column1].tolist()
    index_de_la_valeur=index_de_la_valeur[0]
st.write(index_de_la_valeur)
###################

# Create an empty DataFrame
ddf = pd.DataFrame()

# Add columns to the DataFrame
ddf['jours'] = [0,1,2,3,4] # You can replace None with any default value you want

# Add more columns as needed

for nh in ["temp_","pr_","wind_","hmudi_"]:
        ddf[nh] = None
for i in range(5):
    for nh in ["temp_","pr_","wind_","hmudi_"]:
        ddf[nh][i] = gdf.at[index_de_la_valeur, nh+str(i)]
# Print the empty DataFrame
if option != "cloud":
    chart_data = pd.DataFrame(ddf, columns=[str(att(option))])
    #old way
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
    col2.plotly_chart(fig,use_container_width=True)
##################

##################
if p=='Variable couleur':
        st.pydeck_chart(pdk.Deck(
            
            initial_view_state=pdk.ViewState(
                latitude=(gdf["lat"][index_de_la_valeur]),
                longitude=(gdf["lon"][index_de_la_valeur]),
                zoom=5,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    'ScatterplotLayer',
                    data=gdf,
                    pickable=True,
                    opacity=0.8,
                    
                    filled=True,
                    radius_scale=10,
                    radius_min_pixels=1,
                    radius_max_pixels=100,
                    line_width_min_pixels=1,
                    get_position='[lon, lat]',
                    get_radius=400,
                    get_fill_color='fill_color1',  # Use the new 'fill_color' column
                    auto_highlight=True,
                ),
            ], 
            tooltip = {
        "html": "<b>Nom commune:</b> "         "  {city_name} \n {cl_0} ",
        "style": {
                "backgroundColor": "steelblue",
                "color": "white"
        },
        
        }
        ,map_provider="mapbox",
        map_style=y,


        ))
elif p=='Symbole Proportionnel':
        st.pydeck_chart(pdk.Deck(
            
            initial_view_state=pdk.ViewState(
                latitude=(gdf["lat"][index_de_la_valeur]),
                longitude=(gdf["lon"][index_de_la_valeur]),
                zoom=10,
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
                    radius_max_pixels=500,
                    line_width_min_pixels=1,
                    get_position='[lon, lat]',
                    get_radius=str(att(option))+str(day),
                    get_fill_color='[255,0,0]',  # Use the new 'fill_color' column
                    auto_highlight=True,
 
            ),
        ], 
        tooltip = {
    "html": "<b>Nom commune:</b> "         "  {Nom_Commun} \n {OBJECTID} ",
    "style": {
            "backgroundColor": "steelblue",
            "color": "white"
    },
        }
        
        ,map_provider="mapbox",
        map_style=y,))
elif p=='3D':
        # here we do 3d representation of data with the same color
    view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)
    st.pydeck_chart(pdk.Deck(
        views=[view],
        
        initial_view_state=pdk.ViewState(
            latitude=32,
            longitude=-5,
            zoom=6,
            pitch=45,
        ),
        parameters={"cull": True},
        #Ici on peut ajouter une infinitée de couche et ler symbology 
        layers=[
        pdk.Layer(
            "ColumnLayer",
            id="OBJECTID",
            data=gdf,
            get_elevation=(str(att(option))+str(day)),
            get_position=["lon", "lat"],
            elevation_scale=1000,
            pickable=True,
            auto_highlight=True,
            radius=2000,
            get_fill_color='[255, 165, 0]',
            ),
            
        ],
        map_provider="mapbox",
        map_style=y,
    ))
elif p=="Grid":
    st.pydeck_chart(pdk.Deck(
    
    initial_view_state=pdk.ViewState(
        latitude=32,
        longitude=-5,
        zoom=5,
        pitch=45,
        bearing=0,
        

    ),
    #Ici on peut ajouter une infinitée de couche et ler symbology 
    layers=[
       pdk.Layer(
    "GridLayer",
    gdf,
    pickable=True,
    extruded=True,
    cell_size=20000,
    elevation_scale=5,
    get_position=["lon", "lat"],
)
        
    ],
     map_provider="mapbox",
        map_style=y,
))


















    





