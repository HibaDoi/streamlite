# Web Mapping: Interactive Geospatial Visualization Using Streamlit

📄 **Related Report:** WEB MAPPING: Streamlit Geospatial  

## Problem Solved  
- Developed an **interactive web mapping application** for **visualizing geospatial data** related to weather attributes (**temperature, humidity, wind, and precipitation**).  
- Integrated **real-time data retrieval** using the **OpenWeather API** to enhance weather mapping.  
- Optimized **geospatial data storage and visualization** using **GeoParquet format** for efficient data handling.  

## Tech Stack  
- **Data Acquisition:** OpenWeather API, JSON, CSV, GeoParquet  
- **Geospatial Processing:** Python (GeoPandas, PyArrow), IDW Interpolation, GeoTIFF, COG (Cloud Optimized GeoTIFF)  
- **Web Mapping & Visualization:** Streamlit, Leafmap, Folium, Pydeck, Deck.gl, D3.js  
- **Cloud Integration:** AWS S3 (Cloud Storage)  

## Key Contributions  
- **Implemented data extraction and transformation pipelines** to process geospatial weather data.  
- **Developed interactive mapping features**, including:  
  - Thematic mapping using **Jenks Natural Breaks Classification**  
  - **Time slider** for visualizing weather data changes over time  
  - **SplitMap comparison tool** for before-after analysis  
  - **Search functionality** based on geographic coordinates  
- **Integrated Cloud Optimized GeoTIFF (COG)** to reduce storage costs and enable efficient cloud-based rendering.  

## Key Results  
✅ **Improved performance** by reducing data processing time from **30 minutes (CSV) to 10 minutes (GeoParquet)**.  
✅ **Enabled dynamic user interaction** with **real-time weather updates and spatial queries**.  
✅ **Successfully visualized 1,505 geospatial data points** across Morocco in an interactive dashboard.  
