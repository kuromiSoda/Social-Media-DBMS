import streamlit as st
from PIL import Image

image = Image.open('User-ER-Diagram.png')

st.set_page_config(
    page_title="ER Diagram",
    page_icon="📋",
)

st.title("ER Diagram")
st.image(image,caption="ER Diagram")