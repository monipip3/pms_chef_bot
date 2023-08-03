import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from st_pages import Page, show_pages, hide_pages
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.recipes
collection = db["ninja_api"]

#cursor = collection.find({"$and":[{"email":email},{"password":pwd_hashed}]})

st.text("TBD")