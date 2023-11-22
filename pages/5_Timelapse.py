import imageio
import os

import streamlit as st
yey=st.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'precipitation'))


if yey=='temperature':
    gif_url = "temp.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
elif yey=='humidite':
    gif_url = "humd.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
else:   
    gif_url = "preci.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
# Display a GIF from a URL



