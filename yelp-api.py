from yelpapi import YelpAPI
from dotenv import load_dotenv
import os

load_dotenv()
yelp_key = os.getenv('YELP_API_KEY')

yelp_api = YelpAPI(yelp_key, timeout_s=3.0)

args = {'term': 'restaurants',
    'location': 'Tampa Bay, FL',
    'limit': 5}

search_results = yelp_api.search_query(**args)

for business in search_results['businesses']:
    print(business['name'])
    print(business['location'])
    print(business['phone'])
    print('---')