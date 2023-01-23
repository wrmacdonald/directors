import requests
import json
import os
from dotenv import load_dotenv

# PLAN
# get data from DB my_following: pid, num_mc
# check the api for new additions
# email/notify about new additions
# update data in DB

# Get env vars
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

# TMDB API - 
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# # DB
# import pymongo
# MONGO_USERNAME = os.getenv('MONGO_USERNAME')
# MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
# conn_str = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.r4iszic.mongodb.net/?retryWrites=true&w=majority"
# client = pymongo.MongoClient(conn_str, serverSelectionTimeoutMS=5000)

# # User Data - in MongoDB
# db = client.directors_db
# user_collection = db.user_collection

# Insert a new User
# userDoc = {
#     "name": {"first": "Wes", "last": "MacDonald"},
#     "pid": [1, 3, 30, 28974],
#     "pid_num_mc": [156, 2, 32, 15]
# }
# user_id = user_collection.insert_one(userDoc).inserted_id
# print(user_id)

# Update user data
# user_collection.find_one_and_update(
#     {"name.last": "MacDonald"},
#     { "$set": {"pid_num_mc": [156, 2, 32, 17]}})

# # Get user data
# user = user_collection.find_one({ "name.last": "MacDonald" })

# for testing without DB
user = {
    "pid": [1, 3, 30, 28974],
    "pid_num_mc": [156, 2, 32, 17]
}


# Iterate through Following list
for i in range(len(user["pid"])):
    pid = user["pid"][i]                       # a person id the user it following (a director)
    pid_num_mc = user["pid_num_mc"][i]         # number of movie credits for that pid

    p_response = requests.get(f"{TMDB_BASE_URL}/person/{pid}?api_key={TMDB_API_KEY}")
    print(p_response.json()['name'])

    pmc_response = requests.get(f"{TMDB_BASE_URL}/person/{pid}/movie_credits?api_key={TMDB_API_KEY}")

    # sort the responses: by increasing release_date, with "" dates @ end
    pmc_res_sorted = sorted(pmc_response.json()['crew'], key=lambda x: (x['release_date'] == "", x['release_date']))
    # print(pmc_res_sorted)

    if (len(pmc_res_sorted) > pid_num_mc):
        for i in range(1, len(pmc_res_sorted) - pid_num_mc + 1):
            print(f"checking pid:{pid}, saved # credits:{pid_num_mc}, found credits:{len(pmc_res_sorted)}.")
            print(f"New Entry from pid:{pid} - {pmc_res_sorted[-i]['original_title']}")
    print("----")



    # no sort
    # if (len(pmc_response.json()["crew"]) > pid_num_mc):
    #     for i in range(1, len(pmc_response.json()["crew"]) - pid_num_mc + 1):
    #         print(f"checking pid:{pid}, saved # credits:{pid_num_mc}, found credits:{len(pmc_response.json()['crew'])}.")
    #         print(f"New Entry from pid:{pid} - {pmc_response.json()['crew'][-i]['original_title']}")
    # print("----")
