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
db = client.ingredients
collection = db["ingredients"]

#cursor = collection.find({"$and":[{"email":email},{"password":pwd_hashed}]})

with open("tmp_phase.txt") as f:
    phase = f.readlines()[0]
    st.text(phase)

st.subheader(f"Below are a list of ingredients / food items recommended to eat during your {phase}")

cursor = collection.find({"Menstrual Phase":phase})
ingredients_df = pd.DataFrame()
if cursor != None:
    for record in cursor:
        tmp_df = tmp_df = pd.DataFrame.from_dict(record,orient="index").T
        ingredients_df = pd.concat([ingredients_df,tmp_df],axis=0)
            #tmp_df = pd.DataFrame.from_dict(v,orient="index").T
            #t.text(tmp_df)
        
        # tmp_df.columns = ["id,ingredient","Phase","Type"]
        # tmp_df = tmp_df[['Ingredient',"Type"]]
        # st.dataframe(tmp_df)
st.dataframe(ingredients_df[['Ingredient','Type']])
