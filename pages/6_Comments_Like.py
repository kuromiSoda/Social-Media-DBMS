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
    c.execute('select * from comment_likes')
    return c.fetchall()

def view_user():
    c.execute('select * from users')
    return c.fetchall()

def view_post_comments():
    c.execute('select * from post_comments')
    return c.fetchall()

def delete_record(Comment_ID,Comment_liked_user_ID):
    c.execute(f'delete from comment_likes where Comment_ID = "{Comment_ID}" and Comment_liked_User_ID ="{Comment_liked_user_ID}" ')
    mydb.commit()

def update(choice,Comment_id,Liked_User_ID):
    c.execute(f'update Comment_likes SET Comment_ID = "{Comment_id}" where Comment_ID = {choice} and Comment_liked_User_ID="{Liked_User_ID}"')
    mydb.commit()
    
def add_data(table_name,Comment_ID,User_ID):
    c.execute(f'INSERT INTO {table_name} (Comment_ID,Comment_liked_User_ID) VALUES ("{Comment_ID}","{User_ID}")')
    mydb.commit()

def get_post(post_id,liked_user_id):
    c.execute(f'select * from comment_likes where Comment_ID = "{post_id}" and Comment_liked_User_ID="{liked_user_id}"')
    return c.fetchall()  

def create():
    data = view_post_comments()
    comment_ids = list(set([i[0] for i in data]))
    comment_ID = st.selectbox('Select the Comment to be liked', comment_ids)
    data_ = view_user()
    user_ids = list(set([i[0] for i in data_]))
    user_ID = st.selectbox('Select the user who wishes to Like the comment', user_ids)
    if st.button("Like Comment ?"):
        add_data("comment_likes",comment_ID,user_ID)
        st.success("Successfully added record!")
        
def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Comment_ID','Comment_Liked_User_ID']))
    Comment_ids = list(set([i[0] for i in data]))
    Comment_ID= st.selectbox('Select the Comment to be unliked', Comment_ids)
    Comment_liked_user_ids = list(set([i[1] for i in data]))
    Comment_liked_user_ID= st.selectbox('Select the User who wishes to unlike the Comment', Comment_liked_user_ids)
    if st.button('Delete Record'):
        delete_record(Comment_ID,Comment_liked_user_ID)
        st.success("Deleted!")
        
def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Comment_ID','Liked_User_ID']))
    Comment_ids = list(set([i[0] for i in data]))
    user_ids = list(set([i[1] for i in data]))
    choice = st.selectbox('Select the Comment to be unliked ',Comment_ids)
    choice1 = st.selectbox('Select the user who is involved in the process',user_ids)
    data = get_post(choice,choice1)
    if data:
        data_ = view_post_comments()
        Comment_ids = [i[0] for i in data_]
        Comment_ID = st.selectbox('Select the New Comment to be  Liked', Comment_ids)
        if Comment_ID == '':
            Comment_ID = data[0][0]
        if st.button("Update"):
            update(choice,Comment_ID,choice1)
            st.success("Updated!")
        
def main():
    st.title("COMMENTS LIKE TABLE")
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
        df = pd.DataFrame(data, columns = ['Comment_ID','Comment_Liked_User_ID'])
        st.dataframe(df)
    
    elif choice == 'Delete':
        st.subheader('Select row to delete')
        delete()
    elif choice == 'Update':
        st.subheader('Select row to update')
        edit()

main()