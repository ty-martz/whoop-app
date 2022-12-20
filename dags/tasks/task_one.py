import requests
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *
from datetime import datetime

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
    
    access_token = r.json()['access_token']
    return access_token


def load_latest_recovery(username, pw, token_url):
    access_token = get_token(username, pw, token_url)

    headers = {
    'Authorization': 'bearer {}'.format(access_token)
    }
    cycle = requests.get("https://api.prod.whoop.com/developer/v1/cycle", headers=headers).json()
    recov = requests.get(f"https://api.prod.whoop.com/developer/v1/cycle/{cycle['records'][0]['id']}/recovery", headers=headers).json()
    recovery_score = recov['score']['recovery_score']
    sleep = requests.get(f"https://api.prod.whoop.com/developer/v1/activity/sleep/{recov['sleep_id']}",
                     headers=headers).json()
    sleep_perf = sleep['score']['sleep_performance_percentage']

    user_email = requests.get("https://api.prod.whoop.com/developer/v1/user/profile/basic", headers=headers).json()['email']

    return int(recovery_score), int(sleep_perf), user_email 


def get_strain_range(recovery_score):
    std = 0.2 * 21
    target = 21 * (recovery_score/100)

    low = target - std
    high = target + std

    if low < 0:
        low = 0
        high = std * 2
    elif high > 21:
        high = 21
        low = 21 - (std * 2)
    
    lohi_range = [round(low, 1), round(high, 1), round(target, 1)]
    return lohi_range


def which_workout():
    weekday = datetime.today().weekday() # 0=Monday
    day_dict = {
        0: {'day': 'Monday', 'workouts': ['Lift', 'Yoga', 'Climb?']}, 
        1: {'day': 'Tuesday', 'workouts': ['Climb', 'Lift?']}, 
        2: {'day': 'Wednesday', 'workouts': ['NP', 'Whoop', 'Climb?']}, 
        3: {'day': 'Thursday', 'workouts': ['Lift', 'Climb', 'Run']}, 
        4: {'day': 'Friday', 'workouts': ['Bike', 'Climb']}, 
        5: {'day': 'Saturday', 'workouts': ['Lift', 'Climb', 'Bike']}, 
        6: {'day': 'Sunday', 'workouts': ['Run', 'Yoga', 'Climb']}
        }

    intro = f"Happy {day_dict[weekday]['day']}!"
    daily_workouts = day_dict[weekday]['workouts']

    return intro, daily_workouts


def send_email(sendgrid_key, to="jacksontmartz@gmail.com", from_id="ty.martz@gatech.edu", email_subject="Daily Whoop Bot", html_content="<p>and easy to do anywhere, even with Python</p>"):
    sg = SendGridAPIClient(api_key=os.environ.get(sendgrid_key))
    from_email = Email(from_id)  # Change to your verified sender
    to_email = To(to)  # Change to your recipient
    subject = email_subject
    content = Content("text/html", html_content)
    mail = Mail(from_email, to_email, subject, content)

    # Get a JSON-ready representation of the Mail object
    mail_json = mail.get()

    # Send an HTTP POST request to /mail/send
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)
    print(response.headers)


def whoop_email_task():

    from dotenv import load_dotenv
    load_dotenv()
    USERNAME = os.environ.get("MY_WHOOP_EMAIL")
    PW = os.environ.get("MY_WHOOP_PW")
    #TOKEN_URL = "https://api.prod.whoop.com/oauth/oauth2/token"
    TOKEN_URL = "https://api-7.whoop.com/oauth/token"
    #SENDGRID_KEY = os.environ.get("SENDGRID_KEY")

    recov_score, sleep_score, user_email = load_latest_recovery(USERNAME, PW, TOKEN_URL)
    strain_range = get_strain_range(recov_score)
    email_intro, workout_list = which_workout()
    workouts = " + ".join(workout_list)

    html_body = f"""
                <h3>{email_intro}</h3>
                <br>
                <p>Here is your recovery info and workout plan:</p>
                <p>You had a {recov_score}% recovery with {sleep_score}% sleep performance</p>
                <p>Your workouts will include: {workouts}</p>
                <p>Target a strain of {strain_range[2]}, or more generally between {strain_range[0]} and {strain_range[1]}</p>
                <br>
                <p>Have a Day!</p>
                """

    send_email(sendgrid_key="SENDGRID_KEY", to=user_email, html_content=html_body)