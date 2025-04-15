import mysql.connector
import streamlit as st
import pandas as pd


mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="social_media_proj"
)
c = mydb.cursor()
def view():
    c.execute('select * from post_comments')
    return c.fetchall()
def view_user():
    c.execute('select * from users')
    return c.fetchall()

def view_tr(pid):
    c.execute("CALL COMM1('{}')".format(pid))
    return c.fetchall()

def view_fr(uid):
    c.execute('select * from friends where User_id="{}"'.format(uid))
    return c.fetchall()

def view_posts(uid):
    c.execute('select * from posts where Posted_User_ID="{}"'.format(uid))
    return c.fetchall()

def delete_record(Comment_id):
    c.execute(f'delete from post_comments where Comment_ID = "{Comment_id}"')
    mydb.commit()

def update(Comment_ID,Comment_Content):
    c.execute(f'select CURDATE()')
    Date = c.fetchall()
    formatted_date = Date[0][0].strftime('%Y-%m-%d %H:%M:%S')
    Date = formatted_date.split(' ')[0]
    c.execute(f'update post_Comments SET Comment_Content = "{Comment_Content}" , Commented_Date = DATE "{Date}" where Comment_ID = {Comment_ID}')
    mydb.commit()
    
def add_data(table_name,Post_ID,Comment_Content,User_ID):
    c.execute(f'select CURDATE()')
    Date = c.fetchall()
    formatted_date = Date[0][0].strftime('%Y-%m-%d %H:%M:%S')
    Date = formatted_date.split(' ')[0]
    c.execute(f'INSERT INTO {table_name} (Post_ID,Commented_Date,Comment_Content,Commented_User_ID) VALUES ("{Post_ID}",DATE"{Date}","{Comment_Content}","{User_ID}")')
    mydb.commit()

def get_post(Comment_id):
    c.execute(f'select * from post_comments where Comment_ID = "{Comment_id}"')
    return c.fetchall()  

def create():
    data = view_user()
    user_ids = [i[0] for i in data]
    User_ID = st.selectbox('Select the user who wants to comment ', user_ids)

    da = view_fr(User_ID)
    f_ids = [i[1] for i in da]
    Fr_ID = st.selectbox('Select the user whose post u want to comment ', f_ids)

    data_ = view_posts(Fr_ID)
    post_ids = [i[0] for i in data_]
    Post_ID = st.selectbox('Select the Post on which the user wants to comment ', post_ids)

   

    Comment_Content = st.text_input("Comment_content:")
    if st.button("Add Comment ?"):
        add_data("post_comments",Post_ID,Comment_Content,User_ID)
        st.success("Successfully added record!")
    da = view_tr(Post_ID)
    df = pd.DataFrame(da, columns = ['POST ID','POSTED USER ID','POST CONTENT','COMMENTED USER ID','COMMENTS'])
    st.dataframe(df)
        
def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Comment_ID','Post_ID', 'Comment_Date', 'Comment_Content', 'Commented_User_ID']))
    Comment_ids = [i[0] for i in data]
    choice = st.selectbox('Select the Comment to be delete', Comment_ids)
    if st.button('Delete Record'):
        delete_record(choice)
        st.success("Deleted!")
                
def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['Comment_ID','Post_ID', 'Commented_Date', 'Comment_Content', 'Commented_User_ID']))
    Comment_ids = [i[0] for i in data]
    choice = st.selectbox('Select the Comment to be Updated',Comment_ids)
    data = get_post(choice)
    if data:
        updated_Comment = st.text_input("Enter new Comment")
        if updated_Comment == '':
            updated_Comment = data[0][3]
        if st.button("Update"):
            update(choice, updated_Comment)
            st.success("Updated!")
        
def main():
    st.title("Posts Table")
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
        df = pd.DataFrame(data, columns = ['Comment_ID','Post_ID', 'Comment_Date', 'Comment_Content', 'Commented_User_ID'])
        st.dataframe(df)
    
    elif choice == 'Delete':
        st.subheader('Select row to delete')
        delete()
    elif choice == 'Update':
        st.subheader('Select row to update')
        edit()

main()