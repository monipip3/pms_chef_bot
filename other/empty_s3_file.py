import boto3

def list_non_empty_objects(bucket_name, prefix=None, profile_name=None):
    session = boto3.Session(profile_name=profile_name)
    s3_client = session.client('s3')

    kwargs = {'Bucket': bucket_name}
    if prefix:
        kwargs['Prefix'] = prefix

    objects = []
    while True:
        response = s3_client.list_objects_v2(**kwargs)
        
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Size'] > 0:
                    objects.append(obj)
        
        # Check if there are more objects to be listed
        if response.get('IsTruncated'):  # True if there are more pages
            kwargs['ContinuationToken'] = response.get('NextContinuationToken')
        else:
            break

    return objects

# Example usage
bucket_name = 'nourishus'
prefix = 'recipeimages'  # Use None if you don't want to filter by prefix
profile_name = 'nourishus'  # Use None if default profile should be used

non_empty_objects = list_non_empty_objects(bucket_name, prefix, profile_name)

# Print non-empty objects
for obj in non_empty_objects:
    print(f"Key: {obj['Key']}, Size: {obj['Size']}")
