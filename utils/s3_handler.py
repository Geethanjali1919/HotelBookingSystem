import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from config import S3_BUCKET_NAME

s3_client = boto3.client('s3')

def create_bucket(bucket_name):
    s3_client = boto3.client('s3')
    existing_buckets = [bucket['Name'] for bucket in s3_client.list_buckets()['Buckets']]
    if bucket_name not in existing_buckets:
        s3_client.create_bucket(Bucket=bucket_name)
        print(f"S3 bucket {bucket_name} created.")
    else:
        print(f"S3 bucket {bucket_name} already exists.")


def upload_image(file_path, object_name):
    """
    Uploads an image to the specified S3 bucket.
    
    Parameters:
    file_path (str): The path of the file to upload.
    object_name (str): The name of the file in the S3 bucket.
    """
    try:
        s3_client.upload_file(file_path, S3_BUCKET_NAME, object_name)
        return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{object_name}"
    except (NoCredentialsError, ClientError) as e:
        print(f"Error uploading to S3: {e}")
        return None

def get_image_url(object_name):
    """
    Retrieves the URL for a stored image.
    
    Parameters:
    object_name (str): The name of the file in the S3 bucket.
    
    Returns:
    str: URL of the image.
    """
    return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{object_name}"

def delete_image(object_name):
    s3_client.delete_object(Bucket=S3_BUCKET_NAME, Key=object_name)

