import boto3

# Create an S3 client
s3 = boto3.client('s3')

# Specify the bucket name and the object (file) to download
bucket_name = 'tampa-ai'

# Specify the filename for the downloaded file
local_filename = 'downloaded_file'

# Download the file
file_key = str(input("file key:"))

# To read the file directly into Python without saving, you can use:
file = s3.get_object(Bucket=bucket_name, Key=f'data/{file_key}')['Body'].read()

# Decode bytes to string and split into lines
lines = file.decode('utf-8')

with open(f'data/{file_key}','w') as outfile:
    outfile.write(lines)