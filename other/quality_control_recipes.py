import streamlit as st
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from PIL import Image
import requests
from io import BytesIO
from urllib.parse import quote_plus
import certifi
ca = certifi.where()




###########For local debugging
username = quote_plus(st.secrets["mongodb"]["mongo_username"])
password = quote_plus(st.secrets["mongodb"]["mongo_pwd"])
db_name = st.secrets["mongodb"]["mongo_dbname"]
uri = f"mongodb+srv://{username}:{password}@{db_name}.ouufw1l.mongodb.net/?retryWrites=true&w=majority"
#Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'),tlsCAFile=certifi.where())
###########


db = client['ingredients']
collection = db['recipes_images_data']
quality_control = db['quality_control_recipes']
already_scored = db['quality_control_recipes']


# Fetch all documents from the read-only view
collection_documents = list(collection.find({}))
already_scored_documents = list(already_scored.find({}))

# Create a dictionary from output2 documents for quick look-up
already_scored_dict = {doc['original_document_id']: doc for doc in already_scored_documents}  # Replace 'reference_field' with actual field name



# Filter readonly_documents based on whether a specific field is null
filtered_documents = [
    doc for doc in collection_documents
    if doc.get('original_document_id') is None or doc['original_document_id'] not in already_scored_dict
]
documents = filtered_documents
total_docs = len(filtered_documents)

# Fetch all documents from the collection
#documents = list(collection.find({}))
# Fetch all documents from the read-only view
#total_docs = len(documents)

# Initialize session state to keep track of the current document index
if 'doc_index' not in st.session_state:
    st.session_state['doc_index'] = 806

# Display the current document
doc = documents[st.session_state['doc_index']]
st.write(f"Document {st.session_state['doc_index'] + 1} of {total_docs}")
st.write(f"Document ID: {doc['_id']}")

# Display S3 image
image_url = doc['image_url']
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))
st.image(img, caption='Image from S3', use_column_width=True)

# Display other fields (arrays) for user to review
for field, values in doc.items():
    if isinstance(values, list):
        #if field == 'instructions':  # Assume the field name for instructions is 'instructions'
            st.write(f"**{field.capitalize()}**:")
            st.markdown("\n".join([f"- {value}" for value in values]))  # Display as bullet list
        #else:
            #st.write(f"{field}: {', '.join(map(str, values))}")

# Add Boolean logic input fields
 # Add Boolean logic input fields
st.text("Check the box if the quality is good for following criteria: ")
image_quality = st.checkbox('Image Quality', key=f"{doc['_id']}_img")
ingredient_quality = st.checkbox('Ingredient Quality', key=f"{doc['_id']}_ingredients")
instructions_quality = st.checkbox('Instructions Quality', key=f"{doc['_id']}_instructions")
top_recipe = st.checkbox('Consider a Top Recipe', key=f"{doc['_id']}_top_recipe")
remove_recipe = st.checkbox('Unusable Recipe', key=f"{doc['_id']}_unusable_recipe")
breakfast_type = st.checkbox('Breakfast',key=f"{doc['_id']}_breakfast_recipe")
lunch_type = st.checkbox('Lunch',key=f"{doc['_id']}_lunch_recipe")
dinner_type = st.checkbox('Dinner',key=f"{doc['_id']}_dinner_recipe")
snack_type = st.checkbox('Snack',key=f"{doc['_id']}_snack_recipe")

# Collect additional input fields as needed
#additional_data = st.text_input('Additional data', key=f"{current_doc['_id']}_additional_data")

# If user confirms, store the input in a writable collection and move to the next document
if st.button('Submit and Next'):
    new_document = {
        'original_document_id': doc['_id'],
        'image_quality': image_quality,
        'ingredient_quality': ingredient_quality,
        'instructions_quality': instructions_quality,
        'top_recipe': top_recipe,
        'remove_recipe' : remove_recipe,
        'breakfast' : breakfast_type,
        'lunch': lunch_type,
        'dinner': dinner_type,
        'snack' : snack_type
        
        }
    
    quality_control.insert_one(new_document)
    st.success(f"Inputs for Document {doc['_id']} saved successfully!")

    # Move to the next document
    if st.session_state['doc_index'] < total_docs - 1:
        st.session_state['doc_index'] += 1
    else:
        st.write("All documents have been reviewed.")
    st.experimental_rerun()  # Refresh the page to show the next document

client.close()

