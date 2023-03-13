import json
import requests
import os

# Env vars
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')

# TMDB API - 
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

def lambda_handler(event, context):
    # Search for a Director
    name_query = event['name_query']
    
    sp_response = requests.get(f"{TMDB_BASE_URL}/search/person?api_key={TMDB_API_KEY}&language=en-US&query={name_query}&page=1&include_adult=false")
    # with open("sp_data.json", "w") as data_file:
    #     json.dump(sp_response.json(), data_file, indent=4, sort_keys=True)
    
    print(f"propably -> name:{sp_response.json()['results'][0]['name']} id:{sp_response.json()['results'][0]['id']}")

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

