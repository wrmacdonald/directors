import requests
import json
import os
from dotenv import load_dotenv
import smtplib 


# Get env vars
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
# Email
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_ADDRESS_RCVR = os.getenv('EMAIL_ADDRESS_RCVR')

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
    "pid_num_mc": [157, 3, 33, 17]
}

# New data dict
dir_updates = {
    'director': [],
    'num_mc': [],
    'title': [],
    'overview': [],
    'release_date': [],
}

# Iterate through Following list
for i in range(len(user["pid"])):
    pid = user["pid"][i]                       # a person id the user it following (a director)
    pid_num_mc = user["pid_num_mc"][i]         # number of movie credits for that pid

    # Get Director's name
    p_response = requests.get(f"{TMDB_BASE_URL}/person/{pid}?api_key={TMDB_API_KEY}")
    dir_name = (p_response.json()['name'])

    # Get Director's movie credits
    pmc_response = requests.get(f"{TMDB_BASE_URL}/person/{pid}/movie_credits?api_key={TMDB_API_KEY}")

    # sort the responses: by increasing release_date, with "" dates @ end
    pmc_res_sorted = sorted(pmc_response.json()['crew'], key=lambda x: (x['release_date'] == "", x['release_date']))

    if (len(pmc_res_sorted) > pid_num_mc):
        for i in range(1, len(pmc_res_sorted) - pid_num_mc + 1):
            dir_updates['director'].append(dir_name)
            dir_updates['num_mc'].append(len(pmc_res_sorted))
            dir_updates['title'].append(pmc_res_sorted[-i]['original_title'])
            dir_updates['overview'].append(pmc_res_sorted[-i]['overview'])
            dir_updates['release_date'].append(pmc_res_sorted[-i]['release_date'])


    # no sort
    # if (len(pmc_response.json()["crew"]) > pid_num_mc):
    #     for i in range(1, len(pmc_response.json()["crew"]) - pid_num_mc + 1):
    #         print(f"checking pid:{pid}, saved # credits:{pid_num_mc}, found credits:{len(pmc_response.json()['crew'])}.")
    #         print(f"New Entry from pid:{pid} - {pmc_response.json()['crew'][-i]['original_title']}")
    # print("----")


# Build up Message
message = ""
for i in range(len(dir_updates['director'])):
    if (i == 0) or (dir_updates['director'][i-1] != dir_updates['director'][i]):
        message += (f"{dir_updates['director'][i]} has the following new projects ({dir_updates['num_mc'][i]} total):\n")
    message += (f"  {pmc_res_sorted[-i]['original_title']} - Releasing: {pmc_res_sorted[-i]['release_date']}\n")
    message += (f"    Overview: {pmc_res_sorted[-i]['overview']}\n")
    message += ("    -\n")


# Encode string that's sent over email is unicode encodable
unicode_message = message.encode('ascii', 'ignore').decode('ascii')

# Send Email if there are updates
if message:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as connection:  
        email_address = EMAIL_ADDRESS
        email_password = EMAIL_PASSWORD
        connection.login(email_address, email_password)
        connection.sendmail(
            from_addr=email_address, 
            to_addrs=EMAIL_ADDRESS, 
            msg=f"subject:Director Updates \n\n {unicode_message}"
        )

