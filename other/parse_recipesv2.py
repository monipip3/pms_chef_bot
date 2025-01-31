from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st 
import os 
import certifi
from urllib.parse import quote_plus
import re
import toml

# Define the path to the custom secrets file
custom_secrets_path = "../.streamlit/secrets.toml"

# Load the TOML file
with open(custom_secrets_path, "r") as secrets_file:
    secrets_data = toml.load(secrets_file)

# Assign loaded secrets to `st.secrets`
st.secrets = secrets_data

def parse_ingredient(ingredient_str):
    """Parses an ingredient string into structured format."""
    
    VALID_UNITS = {'ts',
        "c", "tb", "pn", "lg", "md", "sm", "cn", "ml", "pk", "sl", "pt", "ds", "kg", "dr", "ga", "loaf", "tub",
        "tsp", "tbsp", "oz", "fl oz", "cup", "cups", "pt", "qt", "gal", "ml", "l", "dl",
        "g", "kg", "mg", "lb", "lbs", "oz", "cl", "mm", "cm", "inch", "in", "stick",
        "pinch", "pn", "dash", "ds", "drop", "dr", "handful", "hf", "piece", "pc", "pcs",
        "slice", "sl", "bunch", "bn", "can", "jar", "pkt", "pack", "pkg", "sheet", "sh",
        "clove", "cv", "sprig", "spr", "stalk", "stk", "bulb", "blb", "head", "hd", "leaf", "lf"
    }
    
    parts = ingredient_str.split(';')
    main_part = parts[0].strip()
    note = parts[1].strip() if len(parts) > 1 else ""
    
    tokens = main_part.split()
    quantity = ""
    unit = ""
    item = ""
    

    if tokens:
        # Identify quantity (handles whole numbers, fractions, and mixed fractions)
        if re.match(r'^[\d/]+$', tokens[0]):
            quantity = tokens.pop(0)
        elif len(tokens) > 1 and re.match(r'^[\d]+$', tokens[0]) and re.match(r'^[\d/]+$', tokens[1]):
            quantity = tokens.pop(0) + ' ' + tokens.pop(0)  # Handles mixed fractions like "1 1/2"
        elif len(tokens) > 2 and re.match(r'^[\d]+$', tokens[0]) and re.match(r'^[\d]+$', tokens[1]) and re.match(r'^[\d/]+$', tokens[2]):
            quantity = tokens.pop(0) + ' ' + tokens.pop(0) + ' ' + tokens.pop(0)  # Handles extended mixe

    if tokens:
        # Identify unit (if it's in the valid units list)
        if tokens[0].lower() in VALID_UNITS:
            unit = tokens.pop(0)

    # Remaining part is the item
    item = " ".join(tokens)
    
    return {"quantity": quantity, "unit": unit, "item": item, "note": note}

def process_recipe(recipe):
    """Processes a recipe document and updates it with structured ingredient and instruction arrays."""
    ingredients_list = recipe.get("ingredients", "").split('|')
    structured_ingredients = [parse_ingredient(ing) for ing in ingredients_list]
    
    instructions_list = [step.strip() for step in recipe.get("instructions", "").split('.') if step.strip()]
    
    return {"ingredientsArray": structured_ingredients, "instructionsArray": instructions_list}

# MongoDB connection
username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
db = client.ingredients
collection = db.recipes

# Fetch all recipes
recipes = collection.find()

# Update each recipe with structured arrays
for recipe in recipes:
    update_data = process_recipe(recipe)
    collection.update_one({"_id": recipe["_id"]}, {"$set": update_data})

print("Database updated successfully!")


# # MongoDB data processing function
# def split_and_update():
#     username = quote_plus(st.secrets["mongodb"]["mongo_username"])
#     password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
#     db_name = st.secrets["mongodb"]["mongo_dbname"]
#     uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"

#     client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
#     db = client.ingredients
#     collection = db.recipesv2

#     cursor = collection.find({})
#     for doc in cursor:
#         if "ingredients" in doc and isinstance(doc["ingredients"], str):
#             data_array = clean_data(doc["ingredients"], delimiter="|", type='ingredients')
#             collection.update_one({"_id": doc["_id"]}, {"$set": {"ingredientsArray": data_array}})

#         if "instructions" in doc and isinstance(doc["instructions"], str):
#             description_array = clean_data(doc["instructions"], delimiter=".")
#             servings_match = re.findall(r'\d+', doc["servings"])
#             servings_num = int(servings_match[0]) if servings_match else None
#             collection.update_many({"_id": doc["_id"]}, {"$set": {"instructionsArray": description_array, "servings_num": servings_num}})

#     client.close()
# Run the process_recipe function from the script on this test input
