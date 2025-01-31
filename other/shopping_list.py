# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
# import streamlit as st
# from urllib.parse import quote_plus
# import certifi
# import os
# import pandas as pd 

# ca = certifi.where()

# # Step 1: Connect to MongoDB
# #client = MongoClient("mongodb://localhost:27017/")  # Update the URI as needed



# ###########For local debugging
# username = quote_plus(st.secrets["mongodb"]["mongo_username"])
# password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
# db_name = st.secrets["mongodb"]["mongo_dbname"]
# uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"
# #Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
# ###########
# db = client.ingredients  # Replace with your database name
# collection = db["recipes_images_data"]  # Replace with your collection name


# # Try to fetch server information to force connection on a lazy client
# client.server_info()
# print("Connected to MongoDB successfully.")

# # Step 2: Query the collection
# data = list(collection.find())  # Retrieve all documents as a list of dictionaries

# # Step 3: Convert to pandas DataFrame
# df = pd.DataFrame(data)


# df.to_csv('./recipes_metadata.csv',index=False)


import re
from collections import Counter
import spacy
from nltk.corpus import stopwords
import nltk
from nltk.util import bigrams
import pandas as pd
import os
import ast  # For safely converting string representation of lists


df = pd.read_csv('./recipes_metadata.csv')
# Convert string representation of lists into actual lists
df["ingredients"] = df["ingredients"].apply(ast.literal_eval)

# Download NLTK stopwords
nltk.download('stopwords')

# Load spaCy English model for POS tagging
nlp = spacy.load("en_core_web_sm")

# Get NLTK stopwords
stopwords = stopwords.words('english')
stopwords.extend(['inch','lg','seeds','cut','ts','taste','boneless','strips','slices','water','clove','sm','cup'])
stopwords_set = set(stopwords)


### BY CYCLE

# # Function to clean and tokenize
# def clean_and_tokenize(ingredient_list):
#     all_unigrams = []
#     for ingredient in ingredient_list:
#         # Remove quantities and special characters
#         cleaned = re.sub(r"[\d/\.]+[a-zA-Z]*", "", ingredient)  # Remove numbers and measurements
#         cleaned = re.sub(r"[^\w\s]", "", cleaned)  # Remove punctuation
#         cleaned = cleaned.lower()  # Convert to lowercase
#         tokens = cleaned.split()  # Tokenize into words
#         all_unigrams.extend(tokens)
#     return all_unigrams

# # Function to filter nouns and count occurrences
# def process_category(group_df):
#     # Combine ingredients for the category
#     category_ingredients = sum(group_df["ingredients"], [])
#     # Clean and tokenize
#     unigrams = clean_and_tokenize(category_ingredients)
#     # Remove stopwords
#     filtered_unigrams = [word for word in unigrams if word not in stopwords_set]
#     # Filter by character count
#     filtered_by_length = [word for word in filtered_unigrams if len(word) >= 2]
#     # POS tagging to keep only nouns
#     doc = nlp(" ".join(filtered_by_length))
#     nouns = [token.text for token in doc if token.pos_ == "NOUN"]
#     # Count unigrams
#     unigram_counts = Counter(nouns)
#     # Get top 25 unigrams
#     top_25 = unigram_counts.most_common(25)
#     # Convert to DataFrame
#     return pd.DataFrame(top_25, columns=["Unigram", "Count"])

# # Process each category
# cycle_phases_dataframes = {}
# for cycle_phase, group in df.groupby("cycle_phase"):
#     cycle_phase_df = process_category(group)
#     cycle_phases_dataframes[cycle_phase] = cycle_phase_df
#     print(f"\nTop 25 Unigrams for Cycle_phase: {cycle_phase}")
#     print(cycle_phase_df)

# # You can save these DataFrames to CSVs or process further
# # Example: Save to CSV
# for cycle_phase, cycle_phase_df in cycle_phases_dataframes.items():
#     cycle_phase_df.to_csv(f"top_25_{cycle_phase}.csv", index=False)


### All phases together

# Step 1: Flatten and clean text
def clean_and_tokenize(ingredient_list):
    all_unigrams = []
    for ingredient in ingredient_list:
        # Remove quantities and special characters
        cleaned = re.sub(r"[\d/\.]+[a-zA-Z]*", "", ingredient)  # Remove numbers and measurements
        cleaned = re.sub(r"[^\w\s]", "", cleaned)  # Remove punctuation
        cleaned = cleaned.lower()  # Convert to lowercase
        tokens = cleaned.split()  # Tokenize into words
        all_unigrams.extend(tokens)
    return all_unigrams

# Combine all ingredient lists
all_ingredients = sum(df["ingredients"], [])
unigrams = clean_and_tokenize(all_ingredients)

# Step 2: Remove stopwords using NLTK stopwords
filtered_unigrams = [word for word in unigrams if word not in stopwords_set]

# Step 3: Filter by character count (keep unigrams with 2 or more characters)
filtered_by_length = [word for word in filtered_unigrams if len(word) >= 2]

# Step 4: POS tagging to keep only nouns
def filter_nouns(unigram_list):
    doc = nlp(" ".join(unigram_list))
    return [token.text for token in doc if token.pos_ == "NOUN"]

nouns = filter_nouns(filtered_by_length)

# Step 5: Count unigrams
#unigram_counts = Counter(nouns)

# Generate bigrams
bigram_list = list(bigrams(nouns))
# Count bigrams
bigram_counts = Counter(bigram_list)

# Display results
print("Filtered Unigrams (Character Count >= 2, NLTK Stopwords Removed, and Nouns):")
#print(unigram_counts)
print(bigram_counts)

top_200 = bigram_counts.most_common(200)
# Convert to DataFrame
top_200_df = pd.DataFrame(top_200, columns=["Bigram", "Count"])

top_200_df.to_csv('./shopping_list_items_top_200.csv',index='False')