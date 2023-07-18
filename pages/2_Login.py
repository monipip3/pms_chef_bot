import streamlit as st
from st_pages import Page, show_pages, hide_pages
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from streamlit_extras.switch_page_button import switch_page
import time
import hashlib

def make_hashes(password):
    password = password.encode()
    return(hashlib.sha3_256(password).hexdigest())

username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]

uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.users
collection = db["user_logins"]

hide_pages(["Create_Account","Profile_Recipes"])


email= st.text_input(":red[Username]",key="username",max_chars=25,help='required')
pwd = st.text_input(":red[Password]",key="pwd",type='password',max_chars=15,help='required')
pwd_hashed = make_hashes(pwd)

if st.button("Login"):
    if email and  pwd:
        cursor = collection.find({"$and":[{"email":email},{"password":pwd_hashed}]})
        if cursor != None:
            for record in cursor:
                if record["email"] == email and record["password"] == pwd_hashed:
                    switch_page("Profile_Recipes")
                else:
                    st.warning("Please try again")
        else:
            st.warning("Please try again")
    else:
        st.warning("Please try again")

time.sleep(1)
client.close()