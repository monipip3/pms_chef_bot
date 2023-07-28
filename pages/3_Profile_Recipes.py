import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from st_pages import Page, show_pages, hide_pages
import pandas as pd

username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.users
collection = db["user_logins"]

# if 'cache' not in st.session_state:
#     cursor = get_cycle_info()
#     for record in cursor:
#         st.session_state.cache = {'last_cycle_date': record["last_cycle_date"], 'period_length': record["period_length"], 'luteal_length': record["luteal_length"],"cycle_length":record["cycle_length"]}

hide_pages(["Create_Account","Login"])


#email = st.session_state["email"]
#pwd_hashed = st.session_state["pwd_hashed"]

st.header("Welcome to your Profile")#

st.subheader("Below are your cycle stats that you have provided.")

tmp_cycle_info = pd.read_csv('tmp_cycle_info.csv',infer_datetime_format=True)


tmp_cycle_info['last_cycle_date'] = pd.to_datetime(tmp_cycle_info['last_cycle_date'] )
tmp_cycle_info['today'] =  pd.Timestamp.utcnow() 
tmp_cycle_info['cycle_day'] = (tmp_cycle_info["today"] - tmp_cycle_info["last_cycle_date"]).dt.days
st.dataframe(tmp_cycle_info)

cycle_day = tmp_cycle_info['cycle_day'].values[0]
period_length = tmp_cycle_info['period_length'].values[0]
cycle_length = tmp_cycle_info['cycle_length'].values[0]


if cycle_day > 40:
    last_cycle_date = st.date_input_input("Please update your latest cycle")
    tmp_cycle_info['last_cycle_date_updated'] = pd.to_datetime(last_cycle_date)
    tmp_cycle_info['cycle_day'] = (tmp_cycle_info["today"] - tmp_cycle_info["last_cycle_date_updated"]).dt.days
    cycle_day = tmp_cycle_info['cycle_day'].values[0]
    st.dataframe(tmp_cycle_info)

if (cycle_day  - cycle_length) < period_length:
    phase = 'menstrual'
elif cycle_day < period_length:
    phase = 'menstrual'
elif cycle_day > period_length and cycle_day < 14:
    phase = 'follicular'
elif cycle_day > 14 and cycle_day < 19:
    phase = 'fertile window'
else:
    phase = 'luteal'


st.subheader(f" According to your cycle info, you are in your {phase} phase")