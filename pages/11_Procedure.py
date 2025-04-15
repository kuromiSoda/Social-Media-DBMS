import mysql.connector
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Procedure",
    page_icon="👤",
)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="social_media_proj"
)

c = mydb.cursor()

st.title("Procedure")
st.write("Display Number of friends per user")
c.execute("CALL NUMBER_OF_FRIENDS()")
df = pd.DataFrame(c.fetchall(), columns=["USER ID","No. of friends"])
st.dataframe(df)