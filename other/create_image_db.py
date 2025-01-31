import boto3
from pymongo import MongoClient, errors
from bson import ObjectId

# AWS S3 configuration
def get_s3_client(profile_name):
    session = boto3.Session(profile_name=profile_name)
    return session.client('s3')

# MongoDB configuration
def get_mongo_collection():
    mongo_client = MongoClient('mongodb+srv://monieats:hKFnNCrK1TFGpcjF@pcosingredients.ouufw1l.mongodb.net/')
    db = mongo_client['ingredients']  # Replace 'my_database' with your database name
    collection = db['recipe_images']     # MongoDB collection to store S3 objects
    return collection, mongo_client

# Function to generate ObjectId from S3 URI
def generate_id_from_object_key(object_key):
    # Example: obj['Key'] = 'path/to/file/your-id-value.txt'
    # Extract 'your-id-value' from the object key
    parts = object_key.split('_')[-1].split('.')
    if len(parts) > 1:
        return parts[0]
    else:
        return None 

# Function to list S3 objects from a specific prefix and insert into MongoDB
def list_objects_from_prefix_and_store_in_mongodb(bucket_name, prefix_to_process, s3_client, collection):
    #try:
        # List all objects within the specified prefix
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix_to_process)
        #print(response)
        # Iterate through objects and insert into MongoDB
    if 'Contents' in response:
        for obj in response['Contents']:
            try:
                print(obj)
                if obj['Size'] == 0:
                    pass
                else:   
                    print(obj)
                    uri = f"https://{bucket_name}.s3.us-east-2.amazonaws.com/{obj['Key']}"
                    #print(uri)
                    image_id = generate_id_from_object_key(obj["Key"])
                    print(image_id)
                    if image_id is None:
                        pass
                    # Insert object URI into MongoDB collection
                    collection.insert_one({
                        '_id': image_id,
                        'bucket_name': bucket_name,
                        'object_key': obj['Key'],
                        'image_url': uri
                    })
                    print(f"Inserted {uri} into MongoDB")
                    # else:
                    #     print(f"No objects found in prefix: {prefix_to_process}")
            except errors.DuplicateKeyError:
                continue
        print(f"Skipping document with _id {image_id} because it already exists")

            #     else:
            # print(f"No objects found in prefix: {prefix_to_process}")
    
    # except errors.DuplicateKeyError:
    #     continue
    #     print(f"Skipping document with _id {image_id} because it already exists")
        
    # except Exception as e:
    #     print(f"This error occured {e}")
        #print(f"Error listing objects in prefix {prefix} of bucket {bucket_name}: {str(e)}")

# Replace 'your-bucket-name' with your actual bucket name
bucket_name = 'nourishus'
aws_profile_name = 'nourishus'  # Replace with your AWS profile name
prefix_to_process = 'recipeimages'      # Replace with the prefix (folder) you want to process

# Get AWS S3 client using specific profile
s3_client = get_s3_client(aws_profile_name)

# Get MongoDB collection
collection, mongo_client = get_mongo_collection()

# Call function to list S3 objects from the specified prefix and insert into MongoDB
list_objects_from_prefix_and_store_in_mongodb(bucket_name, prefix_to_process, s3_client, collection)

# Close MongoDB connection
mongo_client.close()