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
            messages=[
                {"role": "system",
                "content": "You are a helpful assistant ."},
                
                {"role": "user", 
                
                "content": f""" Here are some examples of questions and answers:
                \n1. What is Tampa known for? -> Tampa is known for its vibrant waterfront parks.\n
                2. When is the best time to visit Tampa? -> The best time is during the spring.
                \nGenerate a question for the answer: {response}"""
                
                }
            ]
        )
        prompt = chat_completion.choices[0].message.content
        
        print(f"Prompt: {prompt}\n Response: {response}")
        prompt_responses[response]= prompt
    
    return(prompt_responses)

prompt_responses = pd.DataFrame(generate_questions(responses))

prompt_responses.head()