import requests
import requests.auth
import os

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

# TODO: add in credential request for tokens

USERNAME = os.environ.get("MY_WHOOP_EMAIL")
PW = os.environ.get("MY_WHOOP_PW")
TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"


def get_token(username, password, token_url):
    r = requests.post(token_url, json={
        "grant_type": "password",
        "issueRefresh": False,
        "password": password,
        "username": username
    })

    # Exit if fail
    if r.status_code != 200:
        print("Fail - Credentials rejected.")
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
recov = requests.get("https://api.prod.whoop.com/developer/v1/recovery", headers=headers).json()
for k,v in recov['records'][0].items():
    print(f"{k} --> {v}")
