import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from st_pages import Page, show_pages, hide_pages


username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.users
collection = db["user_logins"]

hide_pages(["Create_Account","Login"])


st.write(st.session_state.cache)

for k in st.session_state.keys():
    st.session_state[k] = st.session_state[k]
    st.text(st.session_state[k])

#email = st.session_state["email"]
#pwd_hashed = st.session_state["pwd_hashed"]


st.header("Welcome to your Profile")#

st.subheader("Below are your cycle stats that you have provided.")

#st.dataframe([st.session_state['last_cycle_date'],st.session_state['period_length'],st.session_state['luteal_length']])

