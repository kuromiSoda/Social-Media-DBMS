import mysql.connector
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Social Media DBMS Project",
    page_icon="💬",
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
    c.execute('select * from posts')
    return c.fetchall()

def delete_record(Post_id):
    c.execute(f'delete from posts where Post_ID = "{Post_id}"')
    mydb.commit()

def update(post_id,Post_Content):
    c.execute(f'update posts SET Post_Content = "{Post_Content}" where Post_ID = {post_id}')
    mydb.commit()
    
def add_data(table_name,Post_User_ID,Post_Date,Post_Content):
    c.execute(f'INSERT INTO {table_name} (Posted_User_ID,Post_Date,Post_Content) VALUES ("{Post_User_ID}",DATE "{Post_Date}","{Post_Content}")')
    mydb.commit()

def get_post(post_id):
    c.execute(f'select * from posts where Post_ID = "{post_id}"')
    return c.fetchall()  

def create():
    data = view_user()
    user_ids = [i[0] for i in data]
    Post_User_ID = st.selectbox('Select the User who wishes to add the post', user_ids)
    Post_Date = st.text_input("Post_Date:")
    Post_Content = st.text_input("Post_Content")
    if st.button("Add Post"):
        add_data("posts",Post_User_ID,Post_Date,Post_Content)
        st.success("Successfully added record!")
        
def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Post_ID', 'Post_User_ID', 'Post_Date', 'Post_Content']))
    post_ids = [i[0] for i in data]
    choice = st.selectbox('Select the Post to be delete', post_ids)
    if st.button('Delete Record'):
        delete_record(choice)
        st.success("Deleted!")
        
def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Post_ID', 'Post_User_ID', 'Post_Date', 'Post_Content']))
    post_ids = [i[0] for i in data]
    choice = st.selectbox('Select the Post to be Updated',post_ids)
    data = get_post(choice)
    if data:
        updated_Content = st.text_input("Enter new Content")
        if updated_Content == '':
            updated_Content = data[0][3]
        if st.button("Update"):
            update(choice, updated_Content)
            st.success("Updated!")

def main():
    st.title("POSTS TABLE")
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
        df = pd.DataFrame(data, columns = ['Post_ID', 'Post_User_ID', 'Post_Date', 'Post_Content'])
        st.dataframe(df)
    
    elif choice == 'Delete':
        st.subheader('Select row to delete')
        delete()
    elif choice == 'Update':
        st.subheader('Select row to update')
        edit()

main()