import mysql.connector
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Users",
    page_icon="👤",
)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="social_media_proj"
)

c = mydb.cursor()

def view():
    c.execute('select * from users')
    return c.fetchall()

def viewGraph():
    res = view()
    df = pd.DataFrame(res,columns=['USER_ID','Email_ID','Phone_Number','Pass_word','First_name','Last_name','City','PinCode','DOB','Gender','Age'])
    with st.expander("Gender Demography"):
        task_df = df['Gender'].value_counts().to_frame()
        task_df = task_df.reset_index()
        print(task_df)
        p1 = px.pie(task_df, names='index', values='Gender')
        st.plotly_chart(p1)

def delete_record(User_id):
    c.execute(f'delete from users where User_ID = "{User_id}"')
    mydb.commit()

def update(user_id, updated_email, updated_Phone_Number, updated_First_Name, updated_Last_Name, updated_City,updated_PinCode):
    c.execute(f'update users SET Email_ID = "{updated_email}", Phone_Number = "{updated_Phone_Number}", First_name = "{updated_First_Name}", Last_name = "{updated_Last_Name}", City = "{updated_City}" , PinCode ="{updated_PinCode}" where User_ID = {user_id}')
    mydb.commit()
    
def add_data(table_name,Email_ID, Phone_Number, password, First_Name,Last_Name,City,PinCode,Dob,Gender):
    c.execute(f'INSERT INTO {table_name} (Email_ID,Phone_Number,Pass_word,First_name,Last_name,City,PinCode,DOB,Gender) VALUES ("{Email_ID}","{Phone_Number}", "{password}","{First_Name}","{Last_Name}","{City}",{PinCode}, DATE "{Dob}","{Gender}")')
    mydb.commit()

def get_user(user_id):
    c.execute(f'select * from users where User_ID = "{user_id}"')
    return c.fetchall()  

def create():
    Email_ID = st.text_input("Email_ID: ")
    phone_no_str = st.text_input("Phone_Number:")
    password = st.text_input("Password: ")
    First_Name = st.text_input("First_Name : ")
    Last_Name = st.text_input("Last_Name : ")
    City= st.text_input("City : ")
    Pin = st.text_input("Pincode : ")
    Dob= st.text_input("DOB : ")
    m = ["F","M"]
    Gender = st.selectbox("Gender :",m)

    try:
        if st.button("Add User"):
            add_data("users",Email_ID, phone_no_str, password, First_Name,Last_Name,City,Pin,Dob,Gender)
            st.success("Successfully added record!")

    except Exception as e:
        print(e)
        st.error("Person must be older than 18.")
        
def delete():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['User_ID', 'Email_ID', 'Phone_Number', 'Pass_word', 'First_name', 'Last_name','City','PinCode','DOB','Gender','Age']))
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select the User to be delete', user_ids)
    if st.button('Delete Record'):
        delete_record(choice)
        st.success("Deleted!")
                
def edit():
    data = view()
    st.dataframe(pd.DataFrame(data, columns = ['User_ID', 'Email_ID', 'Phone_Number', 'Pass_word', 'First_name', 'Last_name','City','PinCode','DOB','Gender','Age']))
    user_ids = [i[0] for i in data]
    choice = st.selectbox('Select the User to be delete',user_ids)
    data = get_user(choice)
    if data:
        updated_email = st.text_input("Enter new email")
        updated_Phone_Number_str = st.text_input("Enter the New Mobile Number")
        updated_First_Name = st.text_input("Enter New First_Name")
        updated_Last_Name = st.text_input("Enter New Last_Name")
        updated_City = st.text_input("Enter New City")
        updated_Pin = st.text_input("Enter New PinCode")
        if updated_email == '':
            updated_email = data[0][1]
        if updated_Phone_Number_str == '':
            updated_Phone_Number_str = data[0][2]
        if updated_First_Name == '':
            updated_First_Name = data[0][4]
        if updated_Last_Name == '':
            updated_Last_Name = data[0][5]
        if updated_City == '':
            updated_City = data[0][6]
        if updated_Pin == '':
            updated_Pin = data[0][7]
        if st.button("Update"):
            update(choice, updated_email, updated_Phone_Number_str, updated_First_Name, updated_Last_Name, updated_City,updated_Pin)
            st.success("Updated!")

def main():
    st.title("USERS TABLE")
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
        df = pd.DataFrame(data, columns = ['User_ID', 'Email_ID', 'Phone_Number', 'Pass_word', 'First_name', 'Last_name','City','PinCode','DOB','Gender','Age'])
        st.dataframe(df)

    elif choice == 'Delete':
        st.subheader('Select row to delete')
        delete()
    elif choice == 'Update':
        st.subheader('Select row to update')
        edit()

main()
