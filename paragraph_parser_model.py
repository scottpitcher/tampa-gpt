from openai import OpenAI
import openai
import os
import pandas as pd
import json
import time
import copy

# Goal: Create a fine-tuned model of GPT 3.5 that reads in a paragraph of information and generates independent lines of information.
# Purpose: When preparing text data for fine-tuning Tampa.AI model, we will need to utilise this model several times; more computationally and financially efficient to fine-tune as compared to few-shot learning

# Steps for this script:
## - Create OpenAI client
## - Use a pretrained GPT 3.5-turbo model to create examples (10-15 as this task is not too technical) for fine-tuning job
## - Check outputs
## - Create .jsonl format for fine-tuning with examples
## - Create fine-tune job and save model for use in data_cleaning.py

# Initializing the openai client for text processing
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Messages template used for few-shots learning to develop more examples for fine-tuning job
message_template = [
        # Initial SYSTEM prompt
        {"role": "system","content": "You are a helpful assistant whose goal is to read in the user's paragraph and break the paragraph into separate lines of independent information, ensuring each line can be read without prior context. Each line should start with a clear subject and avoid using pronouns that refer to other lines."},    
        # Ex. USER input 1
        {"role": "user","content": "Obtain and write out all independent points of information in the following paragraph: Tampa is famous for its vibrant waterfront parks, beautiful sunsets, and lively cultural scene. The best time to visit is during spring."},
        # Ex. ASSISTANT output 1
        {"role": "assistant","content":"Tampa is famous for vibrant waterfront parks.\nTampa has beautiful sunsets.\nTampa has a lively cultural scene.\nThe best time to visit Tampa is during spring."},
        # Ex. USER input 2
        {"role": "user","content": "Obtain and write out all independent points of information in the following paragraph: New York City, a city within New York State, is the most populated city in the country. Even though the city is expensive to live in, there are many things to do there!"},
        # Ex. ASSISTANT output2
        {"role": "assistant","content":"New York City is a city within New York State.\nNYC is the most populated city in the United States.\nNYC is expensive to live in.\nDespite the high cost of living, there are many things to do in NYC!"},
        # USER input
        {"role": "user", "content": "Obtain and write out all independent points of information in the following paragraph: "}]


def text_processing(line):
    """Creating a function to read in the paragraphs and break them up into lines using few-shot learning"""
    messages = copy.deepcopy(message_template)
    messages[5]["content"] += line
    # print("\nmessage:",messages[5]["content"],"\n")

    chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=messages
    )

    new_line = chat_completion.choices[0].message.content
    # print("\nnew line: ",new_line,"\n")
    return new_line


# text_processing("Downtown Tampa is undergoing significant development and redevelopment in line with a general national trend toward urban residential development. In April 2007, the Tampa Downtown Partnership noted development proceeding on 20 residential, hotel, and mixed-use projects.[128] Many of the new downtown developments were nearing completion in the midst of a housing market slump, which caused numerous projects to be delayed or revamped, and some of the 20 projects TDP lists have not broken ground and are being refinanced.")
# text_processing("New York, often called New York City[b] or simply NYC, is the most populous city in the United States, located at the southern tip of New York State on one of the world's largest natural harbors. The city comprises five boroughs, each of which is coextensive with a respective county. New York is a global center of finance[10] and commerce, culture and technology,[11] entertainment and media, academics and scientific output,[12] and the arts and fashion, and, as home to the headquarters of the United Nations, is an important center for international diplomacy.[13][14][15][16][17] New York City is the center of the world's principal metropolitan economy.[18]")

# Random assortment of paragraphs from Wikipedia
paragraphs = ["Downtown Tampa is undergoing significant development and redevelopment in line with a general national trend toward urban residential development. In April 2007, the Tampa Downtown Partnership noted development proceeding on 20 residential, hotel, and mixed-use projects.[128] Many of the new downtown developments were nearing completion in the midst of a housing market slump, which caused numerous projects to be delayed or revamped, and some of the 20 projects TDP lists have not broken ground and are being refinanced.",
              "New York, often called New York City[b] or simply NYC, is the most populous city in the United States, located at the southern tip of New York State on one of the world's largest natural harbors. The city comprises five boroughs, each of which is coextensive with a respective county. New York is a global center of finance[10] and commerce, culture and technology,[11] entertainment and media, academics and scientific output,[12] and the arts and fashion, and, as home to the headquarters of the United Nations, is an important center for international diplomacy.[13][14][15][16][17] New York City is the center of the world's principal metropolitan economy.[18]",
              "The Tampa Bay area has a humid subtropical climate (Köppen Cfa), although due to its location on the Florida peninsula on Tampa Bay and the Gulf of Mexico, it shows some characteristics of a tropical climate. Tampa's climate generally features hot and humid summers with frequent thunderstorms and dry and mild winters. Average highs range from 71 to 91 °F (22 to 33 °C) year round, and lows 53 to 77 °F (12 to 25 °C). The city of Tampa is split between two USDA climate zones. According to the 2012 USDA Plant Hardiness Zone Map, Tampa is listed as USDA zone 9b north of Kennedy Boulevard away from the bay and 10a near the shorelines and in the interbay peninsula south of Kennedy Boulevard. Zone 10a is about the northern limit of where coconut palms and royal palms can be grown, although some specimens do grow in northern Tampa. Recently, certain palm tree species in the area, along with the rest of the state, have been and continue to be severely affected by a plant disease called Texas phoenix palm decline, which has caused a considerable amount of damage to various local palm tree landscapes and threatens the native palm tree species in the region.",
              "Though threatened by tropical systems almost every hurricane season (which runs from June 1 to November 30), Tampa seldom feels major effects from tropical storms or hurricanes. No hurricane has made landfall in the immediate Tampa Bay area since the category 4 1921 Tampa Bay hurricane made landfall near Tarpon Springs and caused extensive damage throughout the region.",
              "Tampa was founded as a military center during the 19th century with the establishment of Fort Brooke. The cigar industry was also brought to the city by Vincente Martinez Ybor, after whom Ybor City is named. Tampa was reincorporated as a city in 1887 following the Civil War. Tampa's economy is driven by tourism, health care, finance, insurance, technology, construction, and the maritime industry.[12] The bay's port is the largest in the state, responsible for over $15 billion in economic impact.[13]",
              "Taylor Alison Swift (born December 13, 1989) is an American singer-songwriter. A subject of widespread public interest with a vast fanbase, she has influenced the music industry, popular culture, and politics through her songwriting, artistry, entrepreneurship, and advocacy.",
              "Tampa has a diverse culinary scene from small cafes and bakeries to bistros and farm-to-table restaurants. The food of Tampa has a history of Cuban, Spanish, Floribbean and Italian cuisines. There are also many Colombian, Puerto Rican, Vietnamese and barbecue restaurants. Seafood is very popular in Tampa, and Greek cuisine is prominent in the area, including around Tarpon Springs. Food trucks are popular, and the area holds the record for the world's largest food truck rally. In addition to Ybor, the areas of Seminole Heights and South Tampa are known for their restaurants.",
              "The Civil War ended in April 1865 with a Confederate defeat. In May 1865, federal troops arrived in Tampa to occupy the fort and the town as part of Reconstruction. They remained until August 1869.[citation needed] During the immediate post-war period, Tampa was a poor, isolated fishing village with about 1000 residents and little industry. Yellow fever, borne by mosquitoes from nearby swamps, broke out several times during the 1860s and 1870s, causing more residents to leave.[44] In 1869, residents voted to abolish the city of Tampa government.[45]",
              "Downtown Tampa is undergoing significant development and redevelopment in line with a general national trend toward urban residential development. In April 2007, the Tampa Downtown Partnership noted development proceeding on 20 residential, hotel, and mixed-use projects.[128] Many of the new downtown developments were nearing completion in the midst of a housing market slump, which caused numerous projects to be delayed or revamped, and some of the 20 projects TDP lists have not broken ground and are being refinanced. Nonetheless, several developments were completed, making downtown into a 24-hour neighborhood instead of a 9 to 5 business district.[129] As of 2010, Tampa residents faced a decline in rent of 2%. Nationally rent had decreased 4%.[130] The Tampa Business Journal found Tampa to be the number two city for real estate investment in 2014.[131]",
              "There are a number of institutions of higher education in Tampa. The city is home to the main campus of the University of South Florida (USF), a member of the State University System of Florida founded in 1956.[193] USF is classified among 'R1: Doctoral Universities – Very high research activity' and is one of only three universities in Florida designated as a Preeminent State Research University.[194][195] As of 2021, USF has the seventh highest undergraduate enrollment in the U.S. with over 51,000 students.[196]"]

# Formattng examples for fine-tuning
system_prompt = message_template[0]["content"]
print(system_prompt)

user_prompt = message_template[5]["content"]
print(user_prompt)

with open("parser_data.jsonl", 'w') as outfile: # Using 'w' instead of 'a' to ensure a blank starting file
# Using the new text_processing function, we will create examples from the paragraphs in the above variables
    for i, line in enumerate(paragraphs):
        print(f"Currently proceessing paragraph: {i+1}\n")
        # print("line:\n",line, "\n\n")
        new_line = text_processing(line)

        # print("new line:\n",new_line, "\n\n")
        example_messages = []
        example_messages.append({"role":"system", "content":system_prompt})
        example_messages.append({"role":"user", "content":(user_prompt+line)})
        example_messages.append({"role":"assistant", "content":new_line})

        processed_lines = json.dumps({"messages":example_messages}) +"\n"
        outfile.write(processed_lines)


# Upload fine-tune files
with open("parser_data.jsonl", 'rb') as file:
    response = client.files.create(
        file = file,
        purpose = "fine-tune",
    )

file_id = response.id
print(f"File uploaded successfully with ID: {file_id}")

# Create fine-tune job
ft_response = client.fine_tuning.jobs.create(
  training_file= str(file_id), 
  model="gpt-3.5-turbo",
)

job_id = ft_response.id
print(f"Job ID: {job_id}")
# Continous status check on the fine-tune job until completion (success or failure)
while True:
    status = client.fine_tuning.jobs.retrieve(job_id).status
    print(f"Fine-tuning job current status: {status}")

    if status in ["succeeded","failed"]:
        break
    time.sleep(30)