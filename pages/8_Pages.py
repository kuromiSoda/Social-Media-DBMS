import mysql.connector
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Social Media DBMS Project",
    page_icon="📄",
)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="social_media_proj"
)

c = mydb.cursor()

def view_user():
    c.execute('select * from users')
    return c.fetchall()
def view():
    c.execute('select * from pages')
    return c.fetchall()

def delete_record(Page_ID):
    c.execute(f'delete from pages where Page_ID = "{Page_ID}"')
    mydb.commit()

def update(Page_ID,Page_bio,Page_Content_no_followers_n_following):
    c.execute(f'update pages SET Page_bio = "{Page_bio}" , Page_Content_no_followers_n_following = "{Page_Content_no_followers_n_following}" where Page_ID = {Page_ID}')
    mydb.commit()
    
def add_data(table_name,Page_user_id,Page_bio,Page_Content_no_followers_n_following):
    c.execute(f'INSERT INTO {table_name} (Page_user_id,Page_bio,Page_Content_no_followers_n_following) VALUES ("{Page_user_id}","{Page_bio}","{Page_Content_no_followers_n_following}")')
    mydb.commit()

def get_post(page_id):
    c.execute(f'select * from pages where Page_ID = "{page_id}"')
    return c.fetchall()  

def create():
    data = view_user()
    user_ids = [i[0] for i in data]
    Page_user_id = st.selectbox('Select the User who wishes to add the Page', user_ids)
    Page_bio = st.text_input("Page_Bio:")
    Page_Content_no_followers_n_following = st.text_input("Page_Content")
    if st.button("Add Post"):
        add_data("pages",Page_user_id,Page_bio,Page_Content_no_followers_n_following)
        st.success("Successfully added record!")
        
def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Page_ID','Page_user_id','Page_bio','Page_Content_no_followers_n_following']))
    Page_ids = [i[0] for i in data]
    choice = st.selectbox('Select the Page to be delete', Page_ids)
    if st.button('Delete Record'):
        delete_record(choice)
        st.success("Deleted!") 
        
def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Page_ID','Page_user_id','Page_bio','Page_Content_no_followers_n_following']))
    page_ids = [i[0] for i in data]
    choice = st.selectbox('Select the Page to be Updated',page_ids)
    data = get_post(choice)
    if data:
        Page_Content = st.text_input("Enter new Content")
        Page_bio = st.text_input("Enter the new bio")
        if Page_Content == '':
            Page_Content = data[0][3]
        if Page_bio == '':
            Page_bio = data[0][2]
        if st.button("Update"):
            update(choice, Page_bio,Page_Content)
            st.success("Updated!")
        
def main():
    st.title("PAGE TABLE")
    menu = ["Add", "View", "Update", "Delete"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == 'Add':
        st.subheader("Enter details")
        try:
            create()
        except Exception as e:
            st.error("Error!"+' '+str(e))
    elif choice == 'View':
        st.subheader("Information in Table")
        try:
            data = view()
        except:
            st.error("Error!")
        df = pd.DataFrame(data, columns = ['Page_ID','Page_user_id','Page_bio','Page_Content'])
        st.dataframe(df)
    
    elif choice == 'Delete':
        st.subheader('Select row to delete')
        delete()
    elif choice == 'Update':
        st.subheader('Select row to update')
        edit()

main()