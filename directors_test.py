import requests
import json
import os
from dotenv import load_dotenv

# Get env vars
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# TMDB API - 
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# Movie
# response = requests.get(f"{TMDB_BASE_URL}/movie/550?api_key={TMDB_API_KEY}")
response = requests.get(f"{TMDB_BASE_URL}/movie/550/credits?api_key={TMDB_API_KEY}")
# data = response.json()
# json.dump(data, "data.json", indent=4)
with open("data.json", "w") as data_file:
    json.dump(response.json(), data_file, indent=4, sort_keys=True)

# Person
p_response = requests.get(f"{TMDB_BASE_URL}/person/1?api_key={TMDB_API_KEY}")
with open("p_data.json", "w") as data_file:
    json.dump(p_response.json(), data_file, indent=4, sort_keys=True)

# Search Person
sp_response = requests.get(f"{TMDB_BASE_URL}/search/person?api_key={TMDB_API_KEY}&language=en-US&query=george&page=1&include_adult=false")
with open("sp_data.json", "w") as data_file:
    json.dump(sp_response.json(), data_file, indent=4, sort_keys=True)

# Person - Movie Credits
pmc_response = requests.get(f"{TMDB_BASE_URL}/person/1/movie_credits?api_key={TMDB_API_KEY}")
# print(len(pmc_response.json()["crew"]))
with open("pmc_data.json", "w") as data_file:
    json.dump(pmc_response.json(), data_file, indent=4, sort_keys=True)

# Movie - lookup by id
id = 89
m_response = requests.get(f"{TMDB_BASE_URL}/movie/{id}?api_key={TMDB_API_KEY}")
with open("m_data.json", "w") as data_file:
    json.dump(m_response.json(), data_file, indent=4, sort_keys=True)

# get the person id you want, and add it to user's following list
# then each day check whether following id's movie credit list has grown
# if has grown, email details of what id was added?
# Monitor Test
pid = 1
pmc_response = requests.get(f"{TMDB_BASE_URL}/person/{pid}/movie_credits?api_key={TMDB_API_KEY}")
p_1 = 150
if (len(pmc_response.json()["crew"]) > p_1):
    for i in range(1, len(pmc_response.json()["crew"]) - p_1 + 1):
        print(f"New Entry from pid:{pid} - {pmc_response.json()['crew'][-i]['original_title']}")
# print(len(pmc_response.json()["crew"]))



# Letterboxd
# r = requests.get('https://api.letterboxd.com/api/v0/films')
# print(r.status_code, r.text)


# Fake Store API - GET All
BASE_URL = 'https://fakestoreapi.com'
# query_params = {
#     "limit": 2
# }
# response = requests.get(f"{BASE_URL}/products", params=query_params)
# print(response.json())

# Fake Store API - POST
# new_product = {
#     "title": 'test product',
#     "price": 13.5,
#     "description": 'lorem ipsum set',
#     "image": 'https://i.pravatar.cc',
#     "category": 'electronic'
# }
# response = requests.post(f"{BASE_URL}/products", json=new_product)
# print(response.json())

# Fake Store API - PUT
# updated_product = {
#     "title": 'updated_product',
#     "category": 'clothing'
# }
# response = requests.put(f"{BASE_URL}/products/21", json=updated_product)
# print(response.json())

# Fake Store API - GET one
# response = requests.get(f"{BASE_URL}/products/1")
# print(response.json())
