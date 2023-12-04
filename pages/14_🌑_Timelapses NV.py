import streamlit as st
yey=st.selectbox(
    'How would you like to choose?',
    ('temperature', 'humidite', 'pression','vent'))


if yey=='pression':
    gif_url = "Apression.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
elif yey=='Ahumidite':
    gif_url = "humidité.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
elif yey=='temperature':   
    gif_url = "Atemp.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
else:   
    gif_url = "Awind.gif"
    st.image(gif_url, caption='Your GIF', use_column_width=True)
# Display a GIF from a URL



