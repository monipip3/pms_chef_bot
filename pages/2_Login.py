import streamlit as st
from st_pages import Page, hide_pages
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from streamlit_extras.switch_page_button import switch_page
import time
import hashlib
import pandas as pd 
import os
import certifi

hide_pages(["Create_Account","Profile","Recipes"])

def make_hashes(password):
    password = password.encode()
    return(hashlib.sha3_256(password).hexdigest())




############For local debugging
# username = quote_plus(st.secrets["mongodb"]["mongo_username"])
# password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
# db_name = st.secrets["mongodb"]["mongo_dbname"]
# uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"
# #Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
############



######### For prod and heroku 
username = os.getenv('mongo_username')
password = os.getenv('mongo_pwd')
db_name = os.getenv('mongo_dbname')
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
#####################


db = client.users
collection = db["user_logins"]



email= st.text_input(":red[email]",max_chars=250,help='required')
pwd = st.text_input(":red[Password]",type='password',max_chars=15,help='required')
pwd_hashed = make_hashes(pwd)
email_hashed = make_hashes(email)

if st.button("Login"):
    if email and  pwd:
        cursor = collection.find({"$and":[{"email":email},{"password":pwd_hashed}]})
        if cursor != None:
            for record in cursor:
                if record["email"] == email and record["password"] == pwd_hashed:
                    @st.cache_data
                    def get_cycle_info(persist=True):
                        client = MongoClient(uri, server_api=ServerApi('1'))
                        db = client.users
                        collection = db["user_logins"]
                        cursor = collection.find({"$and":[{"email":email},{"password":pwd_hashed}]})
                        return(cursor)
                    # Instantiate the Session State Variables
                    if 'cache' not in st.session_state:
                        
                        st.session_state.cache = {'last_cycle_date': record["last_cycle_date"], 'period_length': record["period_length"], 'luteal_length': record["luteal_length"],"cycle_length":record["cycle_length"]}
                        #st.write(st.session_state.cache)
                        tmp_cycle_df = pd.DataFrame(st.session_state.cache,index=[0])
                        tmp_cycle_df.to_csv('tmp_cycle_info.csv',index=False)
                        #st.dataframe(tmp_cycle_df)


                    switch_page("Profile")
                else:
                    st.warning("Please try again")
        else:
            st.warning("Please try again")
    else:
        st.warning("Please try again")




time.sleep(1)
client.close()
