import boto3
from openai import OpenAI
import os
import pandas as pd

# Goal: Using the paragraph parsing model created in the respective script, we will use that to loop over all raw paragraphs of text data to create independent lines of information about Tampa.
# Purpose: To create response data for the fine-tuning job. 

# Steps for this script:
## - Create OpenAI client
## - Load in fine-tuned model from paragraph_parser_model
## - Loop over all text data in the /data folder in the AWS S3 bucket
## - Save those lines of informatio to another S3 bucket /cleaned_data



## Retrieving web-scraped data from AWS S3 bucket
# Create an S3 client
s3 = boto3.client('s3')
bucket_name = 'tampa-ai'

# Initializing the openai client for text processing
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def break_up_text(text):
    """
    If a list of strings is inputted, it will loop through each element and return it as a full body of text
    Else if a single string is inputted, it will process that string and return the indidivual information from it
    """
    if isinstance(text, list):
        new_text = ""
        
        # Loop through every item of the list, and adding that to a main corpus
        for line in text:
            if len(line) < 10:
                continue
            new_lines = text_processing(line)
            print(f"input:\n{line}\noutput:\n{new_lines}")
            new_text += new_lines       
        
        return(new_text)
    
    elif isinstance(text, str):      
        new_lines = text_processing(text)
        print(f"input:\n{text}\noutput:\n{new_lines}")
        
        return (new_lines)
    
    else:
        # Error warning if neither supported data type is inputted
        return ("Unsupported data type")

break_up_text("Tampa is part of the Tampa-St. Petersburg-Clearwater, Florida Metropolitan Statistical Area, which is a four-county area composed of roughly 3.1 million residents,[14] making it the second-largest metropolitan statistical area (MSA) in the state and the sixth largest in the Southeastern United States, behind Dallas-Fort Worth, Houston, Washington D.C., Atlanta, and Miami.[15] The Greater Tampa Bay area has over 4 million residents and generally includes the Tampa and Sarasota metro areas.")

# Initialising paginator for higher file volumes in bucket
paginator = s3.get_paginator("list_objects_v2")
# Getting pages from the bucket
pages = paginator.paginate(Bucket=bucket_name, Prefix='data/')

def main():
    for page in pages:
        for file in page["Contents"]:
            file_key = file["Key"].split('data/')[-1]
            
            if not file_key.endswith(".txt"):
                continue
            try:
                file_text = s3.get_object(Bucket=bucket_name, Key=file["Key"])['Body'].read()
                # Decode bytes to string and split into lines
                lines = file_text.decode('utf-8').split("\n")
                parsed_text = break_up_text(lines)

                response = s3.put_object(Body = parsed_text, Bucket = bucket_name, Key = f"cleaned_data/{file_key}")
                print(f"Processed {file_key}")
            
            except Exception as e:
                print(f"Failed to process {file_key}: {str(e)}")



if __name__=="__main__":
    main()