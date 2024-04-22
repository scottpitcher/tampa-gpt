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
def text_processing(line):
    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system",
        "content": """You are a helpful assistant whose goal is to break up paragraphs into separate lines with independent information,
             ensuring each line can be read without needing context from the input or other lines. Each line should start with a clear subject 
             and avoid using pronouns that refer to previously mentioned subjects."""},        
        {"role": "user", 
        
        "content": f"""The following are examples of paragraphs broken into separate lines:
        Input paragraph: 'Tampa is famous for its vibrant waterfront parks, beautiful sunsets, and lively cultural scene. The best time to visit is during spring.'
        Output points:
        Tampa is famous for vibrant waterfront parks.
        Tampa has beautiful sunsets.
        Tampa has a lively cultural scene.
        The best time to visit Tampa is during spring.       
        Input paragraph: 'New York City, a city within New York State, is the most populated in the country. Even though the city is expensive to live in, there are many things to do there!'
        Output points:
        New York City is a city within New York State.
        NYC is the most populated city in the United States.
        NYC is expensive to live in.
        Despite the high cost of living, there are many things to do in NYC!

        Now, please break down this paragraph into independent lines of information: {line}"""
        }
    ]
)
    new_line = chat_completion.choices[0].message.content
    return new_line


# If a list of strings is inputted, it will loop through each element and return it as a full body of text
# Else if a single string is inputted, it will process that string and return the indidivual information from it
def break_up_text(text):
    if isinstance(text, list):
        new_text = ""
        
        # Loop through every item of the list, and adding that to a main corpus
        for line in text:
            if len(line) < 10:
                continue
            new_lines = text_processing(line)
            print(f"input:{line}\noutput:{new_lines}")
            new_text += new_lines       
        
        return(new_text)
    
    elif isinstance(text, str):      
        new_lines = text_processing(text)
        print(f"input:{text}\noutput:{new_lines}")
        
        return (new_lines)
    
    else:
        # Error warning if neither supported data type is inputted
        return ("Unsupported data type")

break_up_text("The city is part of the Tampa-St. Petersburg-Clearwater, Florida Metropolitan Statistical Area, which is a four-county area composed of roughly 3.1 million residents,[14] making it the second-largest metropolitan statistical area (MSA) in the state and the sixth largest in the Southeastern United States, behind Dallas-Fort Worth, Houston, Washington D.C., Atlanta, and Miami.[15] The Greater Tampa Bay area has over 4 million residents and generally includes the Tampa and Sarasota metro areas.")

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