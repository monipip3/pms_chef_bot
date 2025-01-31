from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st
from urllib.parse import quote_plus
import certifi
import os

ca = certifi.where()

# Step 1: Connect to MongoDB
#client = MongoClient("mongodb://localhost:27017/")  # Update the URI as needed



###########For local debugging
username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"
#Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
###########
db = client.ingredients  # Replace with your database name
collection = db["recipes"]  # Replace with your collection name


# Try to fetch server information to force connection on a lazy client
client.server_info()
print("Connected to MongoDB successfully.")

# Step 2: Define the lists of keywords
gluten_containing = gluten_containing = [
    "wheat", "barley", "rye", "triticale", "malt", "yeast", "bread", 
    "flour", "crackers", "breadcrumbs", "pasta", "noodles", "cakes", 
    "cookies", "muffins", "pastries", "cereal", "couscous", 
    "dumplings", "farro", "graham flour", "gravy", "matzo", 
    "seitan", "semolina", "spelt", "sauces", "soy sauce", 
    "starch", "tortillas", "beer", "ale", "brewer's yeast", 
    "durum", "kamut", "faro", "roux", "graham cracker", "graham crumbs", "dough"
]

dairy_containing = [ "milk","skim milk", "whole milk", "cream", "butter", "yogurt", "cheese", "cream cheese", 
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
nut_containing = [
    "peanuts", "almonds", "cashews", "walnuts", "pecans", 
    "pistachios", "hazelnuts", "macadamia nuts", "brazil nuts", 
    "pine nuts", "chestnuts"
]
meat_containing = [
    "beef", "pork", "chicken", "lamb", "turkey", "duck", "goose", 
    "veal", "rabbit", "game", "bacon", "ham", "sausage", 
    "pepperoni", "salami", "chorizo", "prosciutto", 
    "pancetta", "bratwurst", "andouille", "kielbasa", 
    "bresaola", "mortadella", "guanciale", "liver", 
    "tripe", "tongue", "pastrami", "corned beef", "venison", 
    "bison", "ostrich", "emu", "quail", "pigeon", "pheasant", 
    "alligator", "frog", "boar", "moose", "elk", "reindeer","steak","sirloin","meat","hamburger","cheeseburger"]
    
fish_containing = ["fish", "catfish", "rockfish", "codfish", "jellyfish", "lobstertail", "monkfish", "salmon", "tuna", "cod", "trout", "halibut", "haddock", "sardines", "mackerel", "anchovies", "swordfish", "mahi Mahi", "tilapia", "shrimp", "crab", "lobster", "clams", "oysters", "scallops", "squid", "calamari", "octopus"]

# Step 3: Define a function to check for keywords in title and ingredients
def check_keywords(title, ingredients, keywords):
    combined_text = f"{title} {' '.join(ingredients)}".lower()
    return any(keyword.lower() in combined_text for keyword in keywords)

# Step 4: Loop through documents and add the new fields
for doc in collection.find():
    #print(doc)
    title = doc.get("title", "")
    ingredients = doc.get("ingredientsArray", [])

    gluten_free = not check_keywords(title, ingredients, gluten_containing)
    dairy_free = not check_keywords(title, ingredients, dairy_containing)
    nut_free = not check_keywords(title, ingredients, nut_containing)
    contains_meat = check_keywords(title, ingredients, meat_containing)
    contains_fish = check_keywords(title, ingredients, fish_containing)
    
    vegetarian = not contains_meat and not contains_fish
    pescatarian = contains_fish and not contains_meat

    # Update the document with new fields
    collection.update_one(
        {"_id": doc["_id"]},
        {"$set": {
            "gluten_free": gluten_free,
            "dairy_free": dairy_free,
            "nut_free": nut_free,
            "vegetarian": vegetarian,
            "pescatarian": pescatarian
        }}
    )

# Step 5: Print completion message
print("Documents updated successfully.")
