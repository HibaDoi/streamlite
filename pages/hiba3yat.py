import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import streamlit as st 
import numpy as np
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show


st.set_page_config(
    page_title="Slideeeer",
    page_icon="🗺️",
)


day = st.slider('witch day', 0, 6, 2)
option = st.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'precipitation'))



d=""
def att(value):
    if value== 'temperature':
        d="temp_j"
    if value== 'humidite':
        d="humd_"
    if value== 'precipitation':
        d="preci_"
    return d 




# Load your GeoDataFrame from Parquet (assuming it has geometry columns)
#gdf = gpd.read_parquet('waaaa.geoparquet')

#on ajoute notre fichier geoparquet
datafile ='waaaa.geoparquet'
#on lit notre fichier geoparquet
data = gpd.read_parquet(datafile)
#add raw data table
geometry = gpd.points_from_xy(data['longitude'], data['latitude'])
gdf = gpd.GeoDataFrame(data, geometry=geometry)
fd=[gdf["latitude"],gdf["longitude"]]
fdd= gpd.GeoDataFrame(fd)

fdd=fdd.transpose()
fdd1=fdd["latitude"]
fdd2=fdd["longitude"]
fdd1=fdd1.values.tolist()
fdd2=fdd2.values.tolist()

temp=[gdf["temp_j0"]]
temp= gpd.GeoDataFrame(temp)

temp= temp.values.tolist()
y= np.array(fdd1)
x= np.array(fdd2)
z = np.array(temp[0])

########################################

# size of the grid to interpolate
nx, ny = 266, 251

# generate two arrays of evenly space data between ends of previous arrays
xi = np.linspace(x.min(), x.max(), nx)
yi = np.linspace(y.min(), y.max(), ny)

# generate grid
xi, yi = np.meshgrid(xi, yi)

# colapse grid into 1D
xi, yi = xi.flatten(), yi.flatten()



##############################################

def distance_matrix(x0, y0, x1, y1):
    """ Make a distance matrix between pairwise observations.
    Note: from <http://stackoverflow.com/questions/1871536>
    """

    obs = np.vstack((x0, y0)).T

    interp = np.vstack((x1, y1)).T


    d0 = np.subtract.outer(obs[:,0], interp[:,0])
    d1 = np.subtract.outer(obs[:,1], interp[:,1])

    # calculate hypotenuse
    return np.hypot(d0, d1)

#####################################################

def simple_idw(x, y, z, xi, yi, power=1):
    """ Simple inverse distance weighted (IDW) interpolation
    Weights are proportional to the inverse of the distance, so as the distance
    increases, the weights decrease rapidly.
    The rate at which the weights decrease is dependent on the value of power.
    As power increases, the weights for distant points decrease rapidly.
    """

    dist = distance_matrix(x,y, xi,yi)

    # In IDW, weights are 1 / distance

    weights = 1.0/(dist+1e-12)**power

    print((weights.shape))
    value_to_replace = 1000000000000.0

    # Create a boolean mask for the value to replace
    mask = weights == value_to_replace

    # Replace the specific value with 0
    weights[mask] = 0

    # Make weights sum to one
    o=weights.sum(axis=0)

    weights = weights/o
    # Multiply the weights for each interpolated point by all observed Z-values
    t=np.dot(weights.T, z)
    a = t
    return a

##############################################################

def plot(x,y,z,grid):
    """ Plot the input points and the result """
    plt.figure(figsize=(15,10))
    plt.imshow(grid, extent=(x.min(), x.max(), y.min(), y.max()), cmap='rainbow', interpolation='gaussian')
    #plt.scatter(x,y,c=z, cmap='rainbow')
    plt.colorbar()

###################################################################

# Calculate IDW
t=str(att(option))+str(day)
temp=[gdf[t]]
temp= gpd.GeoDataFrame(temp)

temp= temp.values.tolist()

z = np.array(temp[0])


grid1 = simple_idw(x,y,z,xi,yi, power=7)
print(grid1)
grid1 = grid1.reshape((ny, nx))
print(grid1)
grid1=grid1[::-1, :]

###################################################################

def read_geotiff(filename):
    ds = gdal.Open(filename)
    band = ds.GetRasterBand(1)
    arr = band.ReadAsArray()
    return arr, ds
##################################################################

def write_geotiff(filename, arr, in_ds):
    if arr.dtype == np.float32:
        arr_type = gdal.GDT_Float32
    else:
        arr_type = gdal.GDT_Int32
    driver = gdal.GetDriverByName("GTiff")
    out_ds = driver.Create(filename, arr.shape[1], arr.shape[0], 1, arr_type)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())
    band = out_ds.GetRasterBand(1)
    band.WriteArray(arr)
    band.FlushCache()
    band.ComputeStatistics(True)
    pixel_size_x = abs(in_ds.GetGeoTransform()[1])
    pixel_size_y = abs(in_ds.GetGeoTransform()[5])
        # Add the creation of the TFW file
    tfw_filename = filename.replace('.tif', '.tfw')
    with open(tfw_filename, 'w') as tfw_file:
        tfw_file.write(f"{pixel_size_x}\n")
        tfw_file.write("0.0\n")  # Rotation values are typically 0
        tfw_file.write("0.0\n")
        tfw_file.write(f"{pixel_size_y}\n")
        tfw_file.write(f"{in_ds.GetGeoTransform()[0]}\n")
        tfw_file.write(f"{in_ds.GetGeoTransform()[3]}\n")

###########################################################

nlcd01_arr, nlcd01_ds = read_geotiff("tif1.tif")


nlcd_changed = grid1

write_geotiff("aahhhee.tif", nlcd_changed, nlcd01_ds)

t="aahhhee.tif"


# from streamlit_folium import folium_static
# import leafmap.foliumap as leafmap
# m = leafmap.Map(height=600, center=[33, -5], zoom=12)
# url = 'aah.tif'
# url2 = 'aah.tif'

# m.split_map(url, url2)
# m
# folium_static(m)
############################################################################
import geopandas as gpd
import rasterio
from rasterio.mask import mask

inshp = 'HHHH.shp'
inRas = t
outRas = 'aahttt.tif'

# Read the shapefile
Vector = gpd.read_file(inshp)
if not Vector.crs:
    print("CRS not defined for the GeoDataFrame. Setting it to EPSG:4326.")
    Vector = Vector.set_crs("EPSG:4326")

with rasterio.open(inRas) as src:
    # Ensure the shapefile and raster have the same CRS
    Vector = Vector.to_crs(src.crs)

    # Clip the raster using the shapefile geometry
    out_image, out_transform = mask(src, Vector.geometry, crop=True)
    out_meta = src.meta.copy()

# Update metadata
out_meta.update({
    "driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform
})
# Write the clipped raster to a new GeoTIFF
with rasterio.open(outRas, 'w', **out_meta) as dst:
    dst.write(out_image)
################################################################

from streamlit_folium import folium_static
import leafmap.foliumap as leafmap

m = leafmap.Map(height=600, center=[33, -5], zoom=12)
url = outRas 
#url="aah.tif"

# Add the raster to the map
try:
    m.add_raster(url, colormap="viridis")
    print(f"Raster added successfully from {url}")
except Exception as e:
    print(f"Error adding raster: {e}")

# Display the map
folium_static(m)





