from openai import OpenAI
import os
import pandas as pd

# Goal: Use the independent lines of information to create prompts for fine-tuning job.
# Purpose: Final set of preparation for model fine-tuning.

# Steps for this script:
## - Load in OpenAI GPT 3.5 turbo model
## - Use pretrained model with few shots learning to create prompts for the responses
## - Utilise data augmentation on prompts to create a diverse set of prompts
## - Format data for finetuning (.jsonl)

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

with open("data.txt", 'r') as infile:
    responses = [infile.readline() for line in infile]

def generate_questions(responses):
    prompt_responses ={}

    for response in responses:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system","content": "You are a helpful assistant whose goal is to create prompts/questions for statements."},              
                {"role": "user", "content": "Create a prompt for the following statement: Tampa is known for its vibrant waterfront parks."},
                {"role": "assistant", "content": "What is Tampa known for?"},
                {"role": "user", "content": "Create a prompt for the following statement: The best time is during the spring."},
                {"role": "assistant", "content": "When is the best time to visit Tampa?"},
                {"role":"user","content":f"Create a prompt for the following statement: {response}"}]
        )
        prompt = chat_completion.choices[0].message.content
        
        prompt_responses[response]= prompt
    
    return(prompt_responses)

prompt_responses = pd.DataFrame(generate_questions(responses))

prompt_responses.head()