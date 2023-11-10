import streamlit as st 
import pymongo
import json 
import os 
import pandas as pd 
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from streamlit_extras.switch_page_button import switch_page
import hashlib
from st_pages import Page, show_pages, hide_pages
import ssl
import certifi

ca = certifi.where()

hide_pages(["Profile","Recipes"])

def make_hashes(password):
    password = password.encode()
    return(hashlib.sha3_256(password).hexdigest())


#username = quote_plus(st.secrets["mongodb"]["mongo_username"])
#password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
#db_name = st.secrets["mongodb"]["mongo_dbname"]

username = os.getenv('mongo_username')
password = os.getenv('mongo_pwd')
db_name = os.getenv('mongo_dbname')


uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())



#update user database with username, password, last cycle date, average cycle length, average period length, average luteal length

st.title("Fill out below to create your account! :seedling:")

st.text('''For the app to be customized, we need some information about your cycle. 
All of this data is anonymized and we do not ask for your name or date of birth.
Your data is secure and not sold to any third party and follows GDPR guidelines.''')


st.subheader(":red[Required Fields]")
email = st.text_input(":red[email]",key="email",max_chars=25,help='required')
pwd = st.text_input(":red[Password]",key="pwd",type='password',max_chars=15,help='required')

pwd_hashed = make_hashes(pwd)

st.subheader(":blue[Optional Fields to improve user experience]")

cycle_dt= st.date_input("Last cycle date YYYY-MM-DD",value = None, key="last_cycle_date",help="Utilized to show you recipes based on your cycle phase")
cycle_length = st.text_input("Average cycle length in days",key="cycle_length",help="Utilized to show you recipes based on your cycle phase")
period_length = st.text_input("Average period length in days",key="period_length",help="Utilized to show you recipes based on your cycle phase")
luteal_length = st.text_input("Average luteal length in days",key="luteal_length",help="Utilized to show you recipes based on your cycle phase")



if st.button("Submit"): 
	user_df = pd.concat([pd.Series(email),pd.Series(pwd_hashed),pd.Series(cycle_dt),pd.Series(cycle_length),pd.Series(period_length),pd.Series(luteal_length)],axis=1)
	user_df.columns = ['email','password','last_cycle_date','cycle_length','period_length','luteal_length']
	user_df['last_cycle_date'] = pd.to_datetime(user_df['last_cycle_date'],utc=True)
	user_df.iloc[:,2:].to_csv('tmp_cycle_info.csv',index=False)
	db = client.users
	collection = db["user_logins"]

	if email and  pwd:
		records = json.loads(user_df.T.to_json(date_format='iso')).values()
		collection.insert_many(records)
		time.sleep(3)
		switch_page("Profile")
	else:
		st.text("Please configure a username and password")
		

time.sleep(2)
client.close()


