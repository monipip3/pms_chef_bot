from pymongo import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st 
import os 
import certifi
from urllib.parse import quote_plus
ca = certifi.where()


def update_phases():
    ###########For local debugging
    username = quote_plus(st.secrets["mongodb"]["mongo_username"])
    password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
    db_name = st.secrets["mongodb"]["mongo_dbname"]
    uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"
    #Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())

    #client = MongoClient("your_mongodb_uri")
    db = client.ingredients
    collection = db.ingredients

    query = { "Menstrual Phase": { "$regex": "Phase$" } }
    update = [
        { 
            "$set": {
                "cycle_phase": {
                    "$replaceAll": { 
                        "input": "$Menstrual Phase", 
                        "find": " Phase", 
                        "replacement": "" 
                    }
                }
            }
        }
    ]

    result = collection.update_many(query, update)
    print(f"Modified {result.modified_count} documents.")

if __name__ == "__main__":
    update_phases()
