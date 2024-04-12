from bs4 import BeautifulSoup
import requests


url = 'https://www.tampabay.com/life-culture/entertainment/2024/04/11/tax-day-tampa-deals-free-april-15/'

def get_article_text(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    paragraphs = soup.find('article').find('section').find_all('p')

    # Iterate through each paragraph, getting the text and appending to the list
    paragraph_texts = [paragraph.get_text() for paragraph in paragraphs]
    
    return paragraph_texts

print(get_article_text(url))
    

