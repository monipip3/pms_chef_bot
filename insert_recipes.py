import pymongo
import json 
import os 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import streamlit as st
from collections import ChainMap


username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))



db = client.ingredients

# list files in recipes to open , read, then insert back into mongodb
recipe_files = os.listdir('./recipes')

recipe_files_w_data = []

for file in recipe_files:
	file = f"./recipes/{file}"
	if os.stat(file).st_size < 10:
		pass
	else:
		recipe_files_w_data.append(file)

#print(len(recipe_files),len(recipe_files_w_data))

# if len(recipe_files) > 0 :
# 	print(" We have recipe files ")


# only insert files that have enough data in it

collection = db["recipes"]

for i in recipe_files_w_data:
	print(f'Opening file data  of {i}')
	with open(f'{i}') as file:
		query = i.split('/')[-1].split('_')[0]
		file_data = json.load(file)
		for recipe_dict in file_data:

		#file_dict = {k:v for list_item in file_data for (k,v) in list_item.items()}
		#file_dict = dict(ChainMap(*file_data))
		#print(file_dict)
		#print(file_dict.keys())
			recipe_dict['query'] = query
	
			#print(recipe_dict.items())
			#print("####################/n")
			#collection.insert_many(recipe_dict)
			collection.insert_one(recipe_dict)
		print(f'Inserted {i} data into DB ')