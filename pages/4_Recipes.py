import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from st_pages import Page, hide_pages
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
import os 
import certifi

ca = certifi.where()

hide_pages(["Create_Account","Login","About"])




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

uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"


db = client.ingredients
collection = db["ingredients"]

#cursor = collection.find({"$and":[{"email":email},{"password":pwd_hashed}]})

with open("tmp_phase.txt") as f:
    phase = f.readlines()[0]
    #st.text(phase)

#st.subheader(f"Below are a list of ingredients / food items recommended to eat during your {phase}")

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
#st.dataframe(ingredients_df[['Ingredient','Type']])

ingredients = list(ingredients_df['Ingredient'].values)
# try:
#     ingredients = ingredients.remove("Brown Rice")
# except ValueError:
#     pass

collection2 = db["recipes_filtered"]


choice = st.selectbox('Pick a food item to look up recipes for',ingredients)


cursor2 = collection2.find({"query":f"{choice}"})
recipes = [record for record in cursor2]


recipes_df = pd.DataFrame(recipes,columns=recipes[0].keys())


recipes_list = recipes_df.title.values

recipe_chosen = st.radio("Pick a recipe",recipes_list)


recipe_ingredients = recipes_df[recipes_df.title == recipe_chosen][['ingredients']].values[0][0].split("|")
recipe_servings = recipes_df[recipes_df.title == recipe_chosen][['servings']].values[0][0]
recipe_instructions = recipes_df[recipes_df.title == recipe_chosen][['instructions']].values[0][0]


st.markdown("## Ingredients")
for i in recipe_ingredients:
    st.markdown(f"+ {i}\n")



st.markdown(f"""
## Servings
{recipe_servings}

## Instructions
{recipe_instructions}



""")
