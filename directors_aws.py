import json
import requests
import os
import smtplib 
import boto3

# Env vars
TMDB_API_KEY = os.environ.get('TMDB_API_KEY')
# Email
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_ADDRESS_RCVR = os.environ.get('EMAIL_ADDRESS_RCVR')
# TMDB API - 
TMDB_BASE_URL = 'https://api.themoviedb.org/3'

# AWS DynamoDB
dynamodb = boto3.resource('dynamodb')
DB_dir1 = dynamodb.Table('directors1')
# print(DB_dir1.creation_date_time)    # Test connection
response = DB_dir1.get_item(
    Key={
        'User': 'Wes'
    }
)
item = response['Item']

def lambda_handler(event, context):
    # Set Run Context
    if event['scheduled']:
        run_context = 'Scheduled'
    else:
        run_context = 'Testing'
        
    # Following Data from DynamoDB
    user = user_creator(item)
    
    # Following Data for testing without DB
    # user = {
    #     "pid": [1, 30, 28974, 1032, 71609, 10491, 118415, 10757, 4762, 68813, 5655, 12453, 21684, 137427],
    #     "pid_num_mc": [158, 33, 18, 167, 19, 39, 42, 47, 50, 20, 52, 78, 51, 32] 
    # }

    # New data dict
    dir_updates = {
        'director': [],
        'pid': [],
        'num_mc': [],
        'title': [],
        'overview': [],
        'release_date': [],
    }

    # Iterate through Following list
    for i in range(len(user["pid"])):
        pid = user["pid"][i]                       # a person id the user is following (a director)
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
                dir_updates['pid'].append(pid)
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
            message += ("-----\n")
            message += (f"{dir_updates['director'][i]} - pid ({dir_updates['pid'][i]}) has the following new projects ({dir_updates['num_mc'][i]} total):\n")
        message += (f"  {dir_updates['title'][i]} - Releasing: {dir_updates['release_date'][i]}\n")
        message += (f"    Overview: {dir_updates['overview'][i]}\n")
        message += ("    -\n")


    # Send Email
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
                msg=f"subject:Director Updates - {run_context} \n\n {unicode_message}"
            )

    print(message)    # Testing
    
    if message: 
        return 'New Movies Found'
    else:
        return 'No New Movies'

def user_creator(user_item):
    # Takes in user_item from dynamoDB & create a matching user dict, with ints
    # in: DynamoDB user Item
    # out: user dict with pid & pid_num_mc fields
    user = {
        "pid": [],
        "pid_num_mc": []
    }
    for i in range(len(user_item['pid'])):
        user['pid'].append(int(user_item['pid'][i]))
        user['pid_num_mc'].append(int(user_item['pid_num_mc'][i]))
    return user
        

