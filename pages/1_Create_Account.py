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


username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]

uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))




#update user database with username, password, last cycle date, average cycle length, average period length, average luteal length

st.title("Fill out below to create your account! :seedling:")

st.text('''For the app to be customized, we need some information about your cycle. 
All of this data is anonymized and we do not ask for your name or date of birth.
Your data is secure and not sold to any third party and follows GDPR guidelines.''')


st.subheader(":red[Required Fields]")
username= st.text_input(":red[Username]",key="username",max_chars=25,help='required')
pwd = st.text_input(":red[Password]",key="pwd",type='password',max_chars=15,help='required')

st.subheader(":blue[Optional Fields to improve user experience]")

cycle_dt= st.date_input("Last cycle date YYYY-MM-DD",value = None, key="last_cycle_date",help="Utilized to show you recipes based on your cycle phase")
cycle_length = st.text_input("Average cycle length in days",key="cycle_length",help="Utilized to show you recipes based on your cycle phase")
period_length = st.text_input("Average period length in days",key="period_length",help="Utilized to show you recipes based on your cycle phase")
luteal_length = st.text_input("Average luteal length in days",key="luteal_length",help="Utilized to show you recipes based on your cycle phase")



if st.button("Submit"): 
	user_df = pd.concat([pd.Series(username),pd.Series(pwd),pd.Series(cycle_dt),pd.Series(cycle_length),pd.Series(period_length),pd.Series(luteal_length)],axis=1)
	user_df.columns = ['username','password','last_cycle_date','cycle_length','period_length','luteal_length']

	db = client.users
	collection = db["user_logins"]

	if username and  pwd:
		records = json.loads(user_df.T.to_json()).values()
		collection.insert_many(records)
		time.sleep(3)
		switch_page("Profile_Recipes")
	else:
		st.text("Please configure a username and password")
		
	client.close()


