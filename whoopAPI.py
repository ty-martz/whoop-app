import requests
import requests.auth
import os
from dotenv import load_dotenv
load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
USERNAME = os.environ.get("MY_WHOOP_EMAIL")
PW = os.environ.get("MY_WHOOP_PW")
#TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
TOKEN_URL = "https://api-7.whoop.com/oauth/token"


def get_token(username, pw, token_url):
    print('')
    r = requests.post(token_url, json={
        "username": username,
        "password": pw,
        "grant_type": "password",
        "issueRefresh": True,
    })    
    # Exit if fail
    if r.status_code != 200:
        print("Fail - Credentials rejected.")
        print('')
        exit()
    else:
        print("Success - Credentials accepted")

    # Set userid/token variables
    userid = r.json()['user']['id']
    access_token = r.json()['access_token']

    return userid, access_token

user_id, access_token = get_token(USERNAME, PW, TOKEN_URL)

headers = {
    'Authorization': 'bearer {}'.format(access_token)
}
print('')
print('-- CYCLE --')
cycle = requests.get("https://api.prod.whoop.com/developer/v1/cycle", headers=headers).json()
for k,v in cycle['records'][0].items():
    print(f"{k} --> {v}")
print('')

print('-- RECOVERY --')
recov = requests.get(f"https://api.prod.whoop.com/developer/v1/cycle/{cycle['records'][0]['id']}/recovery", headers=headers).json()
for k,v in recov.items():
    print(f"{k} --> {v}")
print('')

print('-- SLEEP --')
sleep = requests.get(f"https://api.prod.whoop.com/developer/v1/activity/sleep/{recov['sleep_id']}",
                     headers=headers).json()

for k,v in sleep.items():
    print(f"{k} --> {v}")