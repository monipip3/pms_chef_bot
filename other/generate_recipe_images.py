#@title Install requirements
from io import BytesIO
#import IPython
import json
import os
#from PIL import Image
import requests
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import pandas as pd
import certifi
import streamlit as st
import re

ca = certifi.where()

# list files in recipes to open , read, then insert back into mongodb
#recipe_files = os.listdir('./recipes')

# @markdown To get your API key visit https://platform.stability.ai/account/keys
STABILITY_KEY = 'sk-uB1d2dWMriZxjraOJ2ZeqkorkTFtAHcDiW4y6XktofTrUzTh'



def send_generation_request(
    host,
    params,
):
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_KEY}"
    }

    # Encode parameters
    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to {host}...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response




############For local debugging
username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"
#Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
############



######### For prod and heroku 
# username = os.getenv('mongo_username')
# password = os.getenv('mongo_pwd')
# db_name = os.getenv('mongo_dbname')
# uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
#####################

uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"


db = client.ingredients
collection = db["ingredients"]



# cursor = collection.find()
# ingredients_df = pd.DataFrame()
# if cursor != None:
#     for record in cursor:
#         tmp_df = tmp_df = pd.DataFrame.from_dict(record,orient="index").T
#         ingredients_df = pd.concat([ingredients_df,tmp_df],axis=0)
#             #tmp_df = pd.DataFrame.from_dict(v,orient="index").T
#             #t.text(tmp_df)
        
#         # tmp_df.columns = ["id,ingredient","Phase","Type"]
#         # tmp_df = tmp_df[['Ingredient',"Type"]]
#         # st.dataframe(tmp_df)
# #st.dataframe(ingredients_df[['Ingredient','Type']])
# print(ingredients_df.head())
# ingredients = list(ingredients_df['Ingredient'].values)
# # try:
# #     ingredients = ingredients.remove("Brown Rice")
# # except ValueError:
# #     pass

collection2 = db["recipes_missing_image"]


cursor2 = collection2.find()
recipes = [record for record in cursor2]


recipes_df = pd.DataFrame(recipes,columns=recipes[0].keys())


recipes_list = recipes_df.title.values
print(len(recipes_list))

## loop through each ingrd

print(recipes_df.head())
print(recipes_df.shape)

recipes_chosen = recipes_df.title.values

for recipe_chosen in recipes_chosen:

    recipe_ingredients = recipes_df[recipes_df.title == recipe_chosen][['ingredients']].values[0][0].split("|")
    recipe_servings = recipes_df[recipes_df.title == recipe_chosen][['servings']].values[0][0]
    recipe_instructions = recipes_df[recipes_df.title == recipe_chosen][['instructions']].values[0][0]
    recipe_id = recipes_df[recipes_df.title == recipe_chosen][['_id']].values[0][0]

    # st.markdown("## Ingredients")
    # for i in recipe_ingredients:
    #     st.markdown(f"+ {i}\n")



    # st.markdown(f"""
    # ## Servings
    # {recipe_servings}

    # ## Instructions
    # {recipe_instructions}



    # """)



    prompt = f"A picture of this recipe title {recipe_chosen} after it has been cooked with the following instructions : {recipe_instructions}." #@param {type:"string"}
    negative_prompt = "" #@param {type:"string"}
    aspect_ratio = "1:1" #@param ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]
    seed = 0 #@param {type:"integer"}
    output_format = "jpeg" #@param ["jpeg", "png"]

    host = f"https://api.stability.ai/v2beta/stable-image/generate/sd3"

    params = {
        "prompt" : prompt,
        "negative_prompt" : negative_prompt,
        "aspect_ratio" : aspect_ratio,
        "seed" : seed,
        "output_format" : output_format,
        "model" : "sd3",
        "mode" : "text-to-image"
    }
    try:
        response = send_generation_request(
            host,
            params
        )
        # Decode response
        output_image = response.content
        finish_reason = response.headers.get("finish-reason")
        seed = response.headers.get("seed")

        if response.status_code == 403:
            raise Exception(f" HTTP {response.status_code}: {response.text}")

        # Check for NSFW classification
        if finish_reason == 'CONTENT_FILTERED':
            raise Warning("Generation failed NSFW classifier")

        #clean up recipe_chosen title to save
        pattern = '[^0-9a-zA-Z]+'
        recipe_chosen = re.sub(f'{pattern}', ' ',recipe_chosen)
        # Save and display result
        generated = f"./recipe_images/{recipe_chosen}_generated_{recipe_id}.{output_format}"
        with open(generated, "wb") as f:
            f.write(output_image)
        print(f"Saved image {generated}")

    except Exception as e:
        with open('./recipes_no_img.txt',"w") as file:
            print(recipe_id,type(recipe_id))
            print(recipe_chosen,type(recipe_chosen))
            file.write(f'{str(recipe_id)}_{recipe_chosen}')
        pass
    print("Continuing")