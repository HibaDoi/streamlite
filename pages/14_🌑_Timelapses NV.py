import streamlit as st
yey=st.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'pression','vent'))


if yey=='pression':
    gif_url = "pression.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
elif yey=='humidite':
    gif_url = "humidité.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
elif yey=='temperature':   
    gif_url = "temp.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
else:   
    gif_url = "wwindd.GIF"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
# Display a GIF from a URL



