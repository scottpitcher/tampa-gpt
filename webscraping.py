from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urljoin
import re


# Resetting the data file when rerunning the script to ensure no duplicates
with open("data.txt", "w") as file:
    pass

# Retrieving all articles from sections of a website
def get_article_urls(domain_section):
    page = requests.get(domain_section)
    soup = BeautifulSoup(page.text, 'html.parser')

    # Find all <a> tags (links)
    article_links = soup.find_all('a', href = True)
    
    # Creating a pattern to ensure only articles from 2010:2024 are chosen
    year_pattern = re.compile(r'/20(?:1[5-9]|2[0-4])/')  # First part of the pattern chooses 201 then anynumber 0-9, second part chooses 202 then any number 0-4


    # Adjust URLs for absolute and relative, utilising the urljoin's abilities
    urls = [urljoin(domain_section, link['href']) for link in article_links]
    
    # Filter URLs to keep only those that are articles (contain a year for publ.) and indeed start with the desired domain_section
    urls = [url for url in urls if year_pattern.search(url) and  url.startswith(domain_section)]
    
    # Ensure no duplicate URLs
    list(set(urls))
    return urls

# Defining a function to scape the paragraph data from a website
def get_article_text(url):
    try:
        page = requests.get(url, timeout=5) # Utilising timeout to make sure we are not overloading the server
        if page.status_code != 200:
            print(f"Status code for main page: {page.status_code}")  # Print status code for debug only if it differs

        soup = BeautifulSoup(page.text, 'html.parser')

        # Retrieving the article's body
        article_body = soup.find('article')
        
        paragraphs = soup.find_all('p')
         # Iterate through each paragraph, getting the text and appending to the list
        paragraph_texts = [paragraph.get_text() for paragraph in paragraphs]
        return paragraph_texts
    
    except Exception as e:
        print(f"An error occured while attempting to scrape {url}: e")
        return None


domain_sections = ['https://www.tampabay.com/life-culture/']

def main():
    for domain_section in domain_sections:
        article_urls = get_article_urls(domain_section)

        for url in article_urls:
            print(f"Scraping article: {url}")
            article_text = get_article_text(url)
            if article_text:
                with open("data.txt", 'a') as outfile:
                    outfile.write(f"{article_text}\n\n")
            
            time.sleep(1) # Ensuring not to overload the website's server
    
if __name__ == "__main__":
    main()
