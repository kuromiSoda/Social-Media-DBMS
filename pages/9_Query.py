import mysql.connector
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Social Media DBMS Project",
    page_icon="❓",
)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="social_media_proj"
)
c = mydb.cursor()

st.title("EXECUTE A QUERY")
query = st.text_input("Enter the Query to be executed: ")
if(query!=''):
    try:
        c.execute('{}'.format(query))
        df2 = c.fetchall()
        st.dataframe(df2)
        st.success("Query Executed Successfully")
    except Exception as e:
        print(e)
        st.error("Query Execution Failed")