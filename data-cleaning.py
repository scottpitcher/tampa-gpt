import boto3
from openai import OpenAI
import os
import pandas as pd

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

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# Creating a function to read in the file and break up paragraphs with a pretrained model
def break_up_text(text_file):
    new_text = ""
    for line in text_file:
        new_line = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                "content": """You are a helpful assistant whose goal is 
                to break up paragraphs into separate lines with indpendent information."""},
                
                {"role": "user", 
                
                "content": f""" Here are some examples of questions and answers:
                1. What is Tampa known for? -> Tampa is known for its vibrant waterfront parks.\n
                2. When is the best time to visit Tampa? -> The best time is during the spring.
                Generate a question for the answer: {line}"""
                
                }
            ]
        )
        new_text += new_line.join("\n")
    
    return(new_text)