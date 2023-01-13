import requests
import json
import os
from dotenv import load_dotenv

# Get env vars
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# TMDB API - 
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Search Person
person_query = "Damon Lindelof"
sp_response = requests.get(f"{TMDB_BASE_URL}/search/person?api_key={TMDB_API_KEY}&language=en-US&query={person_query}&page=1&include_adult=false")
with open("sp_data.json", "w") as data_file:
    json.dump(sp_response.json(), data_file, indent=4, sort_keys=True)

print(f"propably -> name:{sp_response.json()['results'][0]['name']} id:{sp_response.json()['results'][0]['id']}")
