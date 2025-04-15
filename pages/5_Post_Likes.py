import mysql.connector
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Social Media DBMS Project",
    page_icon="👍",
)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="social_media_proj"
)

c = mydb.cursor()

def view():
    c.execute('select * from post_likes')
    return c.fetchall()

def view_user():
    c.execute('select * from users')
    return c.fetchall()
def view_post():
    c.execute('select * from posts')
    return c.fetchall()

def delete_record(Liked_User_ID,Post_id):
    c.execute(f'delete from post_likes where Post_ID = "{Post_id}" and Liked_User_ID ="{Liked_User_ID}" ')
    mydb.commit()

def update(choice,post_id,Liked_User_ID):
    c.execute(f'update post_likes SET Post_ID = "{post_id}" where Post_ID = {choice} and Liked_User_ID="{Liked_User_ID}"')
    mydb.commit()
    
def add_data(table_name,Liked_User_ID,Post_ID):
    c.execute(f'INSERT INTO {table_name} (Post_ID,Liked_User_ID) VALUES ("{Post_ID}","{Liked_User_ID}")')
    mydb.commit()

def get_post(post_id,liked_user_id):
    c.execute(f'select * from post_likes where Post_ID = "{post_id}" and Liked_User_ID="{liked_user_id}"')
    return c.fetchall()  

def create():
    data = view_user()
    user_ids = list(set([i[0] for i in data]))
    Liked_User_ID = st.selectbox('Select the User who wishes to like the post', user_ids)
    data_ = view_post()
    post_ids = list(set([i[0] for i in data_]))
    Post_ID = st.selectbox('Select the Post which the user wishes to Like', post_ids)
    if st.button("Like Post ?"):
        add_data("post_likes",Liked_User_ID,Post_ID)
        st.success("Successfully added record!")

def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Post_ID','Liked_User_ID']))
    post_ids = list(set([i[0] for i in data]))
    Post_ID= st.selectbox('Select the shared Post to be unliked', post_ids)
    liked_user_ids = list(set([i[1] for i in data]))
    Liked_user_ID= st.selectbox('Select the User who wishes to unlike the post', liked_user_ids)
    if st.button('Delete Record'):
        delete_record(Liked_user_ID,Post_ID)
        st.success("Deleted!")
        
def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Post_ID','Liked_User_ID']))
    post_ids = list(set([i[0] for i in data]))
    user_ids = list(set([i[1] for i in data]))
    choice = st.selectbox('Select the Post to be Like an Other Post ',post_ids)
    choice1 = st.selectbox('Select the user who is involved in the process',user_ids)
    data = get_post(choice,choice1)
    if data:
        data_ = view_post()
        post_ids = [i[0] for i in data_]
        Post_ID = st.selectbox('Select the New Post to be  Liked', post_ids)
        if Post_ID == '':
            Post_ID = data[0][0]
        if st.button("Update"):
            update(choice,Post_ID,choice1)
            st.success("Updated!")

def main():
    st.title("POST LIKES TABLE")
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
        df = pd.DataFrame(data, columns = ['Post_ID','Liked_User_ID'])
        st.dataframe(df)
    
    elif choice == 'Delete':
        st.subheader('Select row to delete')
        delete()
    elif choice == 'Update':
        st.subheader('Select row to update')
        edit()

main()