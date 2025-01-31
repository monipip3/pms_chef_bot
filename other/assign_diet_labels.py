from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import os 
import certifi
from urllib.parse import quote_plus
import streamlit as st
import re
ca = certifi.where()


###########For local debugging
username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"
#Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
###########





def assign_labels(ingredients):
    labels = []
    
    # List of ingredients containing gluten
    gluten_containing = ["wheat", "barley", "rye", "triticale", "malt", "yeast","bread","bread crumbs","breadcrumbs","pasta","noodles","soy sauce"]
    
    # List of ingredients containing dairy
    dairy_containing = [ "milk", "cream", "butter", "yogurt", "cheese", "cream cheese", 
    "sour cream", "buttermilk", "half and half", "whipped cream", 
    "ice cream", "feta", "mozzarella", "cheddar", "parmesan", 
    "gouda", "brie", "camembert", "ricotta", "mascarpone", 
    "gruyere", "blue cheese", "stilton", "roquefort", "gorgonzola", 
    "pecorino", "asiago", "fontina", "havarti", "colby", "monterey jack", 
    "provolone", "swiss", "edam", "emmental", "muenster", "taleggio", 
    "limburger", "paneer", "queso blanco", "queso fresco", 
    "cotija", "halloumi", "manchego", "boursin", "reblochon", 
    "vacherin", "neufchatel", "chèvre", "chevre", "chèvre frais", 
    "chevre frais", "tomme", "comté", "grana padano", "raclette", 
    "taleggio", "beaufort", "caerphilly", "cheshire", "wensleydale", 
    "double gloucester", "red leicester", "smoked gouda", 
    "leicester", "leicester cheese", "red windsor", "port salut", 
    "pont-l'évêque", "reblochon", "langres", "epoisses", 
    "brillat-savarin", "saint-andré", "boursault", "chaource", 
    "mont d'or", "saint-marcellin", "crottin de chavignol", 
    "stinking bishop", "casu marzu", "whey", "clotted cream", 
    "creme fraiche", "ghee", "evaporated milk", "condensed milk", 
    "kefir", "quark", "labneh", "skyr", "butterfat", "casein", 
    "whey protein", "milk powder", "custard", "pudding"]
    
    # List of ingredients containing nuts
    nut_containing = ["peanuts", "almonds", "cashews", "walnuts", "pecans", "pistachios", "hazelnuts"]
    
    # List of ingredients containing meat
    meat_containing = [
    "beef", "pork", "chicken", "lamb", "turkey", "duck", "goose", 
    "veal", "rabbit", "game", "bacon", "ham", "sausage", 
    "pepperoni", "salami", "chorizo", "prosciutto", 
    "pancetta", "bratwurst", "andouille", "kielbasa", 
    "bresaola", "mortadella", "guanciale", "liver", 
    "tripe", "tongue", "pastrami", "corned beef", "venison", 
    "bison", "ostrich", "emu", "quail", "pigeon", "pheasant", 
    "alligator", "frog", "boar", "moose", "elk", "reindeer","steak","sirloin","meat","hamburger","cheeseburger"]
    
    #list containing fish
    fish_containing = [
    "fish",
    "catfish",
    "rockfish",
    "codfish",
    "jellyfish",
    "lobstertail",
    "monkfish",
    "salmon",
    "tuna",
    "cod",
    "trout",
    "halibut",
    "haddock",
    "sardines",
    "mackerel",
    "anchovies",
    "swordfish",
    "mahi Mahi",
    "tilapia",
    "shrimp",
    "crab",
    "lobster",
    "clams",
    "oysters",
    "scallops",
    "squid",
    "calamari",
    "octopus"
]

    # Check for gluten-containing ingredients
    if any(ingredient in gluten_containing for ingredient in ingredients):
        labels.append("Contains Gluten")
    
    # Check for dairy-containing ingredients
    if any(ingredient in dairy_containing for ingredient in ingredients):
        labels.append("Contains Dairy")
    
    # Check for nut-containing ingredients
    if any(ingredient in nut_containing for ingredient in ingredients):
        labels.append("Contains Nuts")
    
    # Check for meat-containing ingredients
    if any(ingredient in meat_containing for ingredient in ingredients):
        labels.append("Contains Meat")

    if any(ingredient in fish_containing for ingredient in ingredients):
         labels.append("Contains Fish")
    else:
        labels.append("Vegetarian")
    
    return labels

def rewrite_labels(labels):
    if "Contains Gluten" not in labels:
        if "Contains Dairy"  not in labels:
            labels.extend(["Gluten-free","Dairy-free"])
            return(labels) 
    elif "Contains Dairy" not in labels:
            labels.append("Dairy-Free")
    elif "Contains Gluten" not in labels:
            labels.append("Gluten-Free")
    else:
        pass
    return(labels)

def process_text(recipe_title,ingredients):
    text = recipe_title + ' '.join(ingredients)
    text = text.lower()
    text = re.sub(r'[^A-Za-z ]+', '', text)
    text = text.split(' ')
    text = [word for word in text if len(word)>2] #at least 2 characters in the wordx
    return(text)

db = client.ingredients
collection = db["recipes"]

#st.subheader(f"Below are a list of ingredients / food items recommended to eat during your {phase}")

cursor = collection.find()
recipe_df = pd.DataFrame()
if cursor != None:
    for record in cursor:
        tmp_df = tmp_df = pd.DataFrame.from_dict(record,orient="index").T
        recipe_df = pd.concat([recipe_df,tmp_df],axis=0)

recipe_df.reset_index(inplace=True,drop=True)
print(recipe_df.head())
recipe_df.head().to_csv('sample_recipes.csv')
#recipe_df.columns = ['_id','title','ingredients','servings','instructions','query']

recipe_df['processed_text'] = recipe_df.apply(lambda x:process_text(x['title'],x['ingredientsArray']),axis=1)
recipe_df['diet_labels'] = recipe_df.processed_text.apply(assign_labels)
#recipe_df['new_labels'] = recipe_df.diet_labels.apply(rewrite_labels)
print(recipe_df.shape)
recipe_df.to_csv('~/Desktop/Github/pms_chef_bot/recipes_df.csv',index=False)