import boto3
from openai import OpenAI
import os
import pandas as pd

# Goal: Create a fine-tuned model of GPT 3.5 that reads in a paragraph of information and generates independent lines of information.
# Purpose: When preparing text data for fine-tuning Tampa.AI model, we will need to utilise this model several times; more computationally and financially efficient to fine-tune as compared to few-shot learning

# Steps for this script:
## - Create OpenAI client
## - Use a pretrained GPT 3.5-turbo model to create examples (10-15 as this task is not too technical) for fine-tuning job
## - Check outputs
## - Create .jsonl format for fine-tuning with examples
## - Create fine-tune job and save model for use in data preparation

## Retrieving web-scraped data from AWS S3 bucket
# Create an S3 client
s3 = boto3.client('s3')
bucket_name = 'tampa-ai'

# Initializing the openai client for text processing
client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)



message_template = [
        # Initial system prompt
        {"role": "system","content": "You are a helpful assistant whose goal is to read in the user's paragraph and break the paragraph into separate lines of independent information, ensuring each line can be read without context from the input or other lines. Each line should start with a clear subject and avoid using pronouns that refer to other lines."},    
        # Ex. user input 1
        {"role": "user","content": f"Tampa is famous for its vibrant waterfront parks, beautiful sunsets, and lively cultural scene. The best time to visit is during spring."},
        # Ex. assistant output 1
        {"role": "assistant","content":"""Tampa is famous for vibrant waterfront parks.
        Tampa has beautiful sunsets.
        Tampa has a lively cultural scene.
        The best time to visit Tampa is during spring."""},
        # Ex. user input 2
        {"role": "user","content": f"New York City, a city within New York State, is the most populated city in the country. Even though the city is expensive to live in, there are many things to do there!"},
        # Ex. assistant output2
        {"role": "assistant","content":"""New York City is a city within New York State.
        NYC is the most populated city in the United States.
        NYC is expensive to live in.
        Despite the high cost of living, there are many things to do in NYC!"""},
        # User input
        {"role": "user", 
        "content": ""}]


def text_processing(line):
    """Creating a function to read in the file and break up paragraphs with a pretrained model"""
    messages=message_template.copy()
    messages[5]["content"] = line

    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )

    new_line = chat_completion.choices[0].message.content
    return new_line

# Creating examples from paragraphs sourced from 
paragraphs = []

# Formattng examples for fine-tuning
system_prompt = message_template[0]["content"]
print(system_prompt)

# Using the new text_processing function, we will create examples from the paragraphs in the above variables
for paragraph in paragraphs:
    print("hi")