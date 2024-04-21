import boto3
from openai import OpenAI
import os
import pandas as pd

## Retrieving web-scraped data from AWS S3 bucket
# Create an S3 client
s3 = boto3.client('s3')
bucket_name = 'tampa-ai'

# Initializing the openai client for text processing
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# Creating a function to read in the file and break up paragraphs with a pretrained model
def break_up_text(text_file):
    new_text = ""
    for line in text_file:
        if len(line) < 10:
            next
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                "content": """You are a helpful assistant whose goal is 
                to break up paragraphs into separate lines with indpendent information."""},
                
                {"role": "user", 
                
                "content": f"""The following is an example of a paragraph broken into separate points:
                Input paragraph: 'Tampa is famous for its vibrant waterfront parks, beautiful sunsets, and lively cultural scene. The best time to visit is during spring.'
                Output points:
                Tampa is famous for vibrant waterfront parks.\n
                Tampa has beautiful sunsets.\n
                Tampa has a lively cultural scene. \n
                The best time to visit Tampa is during spring.\n

                Now, please break down this paragraph into separate points of information: {line}"""
                }
            ]
        )
        new_line = chat_completion.choices[0].message.content
        print(f"input:{line}\noutput:{new_line}")

        new_text += new_line.join("\n")
    
    return(new_text)



# Initialising paginator for higher file volumes in bucket
paginator = s3.get_paginator("list_objects_v2")
# Getting pages from the bucket
pages = paginator.paginate(Bucket=bucket_name, Prefix='data/')

def main():
    for page in pages:
        for file in page["Contents"]:
            file_key = file["Key"].split('data/')[-1]
            print(file_key)
            file_text = s3.get_object(Bucket=bucket_name, Key=file)['Body'].read()
            # Decode bytes to string and split into lines
            lines = file_text.decode('utf-8').split("\n")
            
            parsed_text = break_up_text(lines)

            response = s3.put_object(Body = parsed_text, Bucket = bucket_name, Key = f"cleaned_data/{file_key}")




if __name__=="__main__":
    main()