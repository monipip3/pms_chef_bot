import boto3



# AWS S3 configuration
def get_s3_client(profile_name):
    session = boto3.Session(profile_name=profile_name)
    return session.client('s3')

# Replace 'your-bucket-name' with your actual bucket name
bucket_name = 'nourishus'
aws_profile_name = 'nourishus'  # Replace with your AWS profile name
prefix = 'recipeimages'      # Replace with the prefix (folder) you want to process

def rename_objects_with_prefix(bucket_name, prefix):
    # Create an S3 client
    s3 = get_s3_client(aws_profile_name)

    # List objects with the specified prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Check if there are any objects to process
    if 'Contents' in response:
        for obj in response['Contents']:
            old_key = obj['Key']
            new_key = old_key.replace(' ', '_')

            if old_key != new_key:
                # Copy the object to a new key
                s3.copy_object(Bucket=bucket_name, CopySource={'Bucket': bucket_name, 'Key': old_key}, Key=new_key)

                # Delete the old object
                s3.delete_object(Bucket=bucket_name, Key=old_key)

                print(f'Renamed object from "{old_key}" to "{new_key}"')
    else:
        print(f'No objects found with prefix "{prefix}"')


rename_objects_with_prefix(bucket_name, prefix)
