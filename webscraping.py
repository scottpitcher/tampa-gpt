from bs4 import BeautifulSoup
import requests
import time
from urllib.parse import urljoin
import re



# Resetting the data file when rerunning the script to ensure no duplicates
with open("data.txt", "w") as file:
    pass

# Returns all URLs from a sitemap, unfiltered
def get_urls_from_sitemap(sitemap_url):
    response = requests.get(sitemap_url)
    soup = BeautifulSoup(response.content)
    urls = [loc.text for loc in soup.find_all('loc')]
    return urls

# Based on prev. function to filter URLs
def filter_urls_by_section_and_date(urls, section):
    filtered_urls = []

    year_pattern = re.compile(r'/20(?:1[5-9]|2[0-4])/')  # First part of the pattern chooses 201 then anynumber 0-9, second part chooses 202 then any number 0-4
    
    for url in urls:
        if section in url:
            match = year_pattern.search(url)
            if match:
                filtered_urls.append(url)
    
    return filtered_urls

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



sitemap_sections = {'https://www.tampabay.com/resources/sitemaps/tampa-bay-times-content-sitemap-48.xml':'/life-culture/'}
sitemap_sections.items()

def main():
    for sitemap, section in sitemap_sections.items():
        urls = get_urls_from_sitemap(sitemap)
        filtered_urls = filter_urls_by_section_and_date(urls, section)

        for url in filtered_urls:
            print(f"Scraping article: {url}")
            article_text = get_article_text(url)
            if article_text:
                with open("data.txt", 'a') as outfile:
                    outfile.write(f"{article_text}\n\n")
            
            time.sleep(1) # Ensuring not to overload the website's server
    
if __name__ == "__main__":
    main()
