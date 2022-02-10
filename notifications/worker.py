import os
from celery import Celery
import httpx
import smtplib, ssl


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

ADVERTISEMENTS_SERVICE_HOST_URL=os.environ.get("ADVERTISEMENTS_SERVICE_HOST_URL")
USERS_SERVICE_HOST_URL=os.environ.get("USERS_SERVICE_HOST_URL")
RELATIONS_SERVICE_HOST_URL=os.environ.get("RELATIONS_SERVICE_HOST_URL")
PORT = 465  # For starttls
SMTP_SERVER = "smtp.gmail.com"
SENDER_EMAIL = "advertisementjnp@gmail.com"
PASSWORD = os.environ.get("PASSWORD")



def get_followers(id: int, type: str):
    r = httpx.get(RELATIONS_SERVICE_HOST_URL + 'followers/'+ type +"/" + str(id))
    return r.json()

def get_users(advertisement_id: int, owner_id: int):
    users_following_advertisement = set([x["user_id"] for x in get_followers(advertisement_id, "advertisement")])
    users_following_owner = set([x["user_id"] for x in get_followers(owner_id, "user")])
    return list(users_following_advertisement | users_following_owner)

def advertisement_to_string(advertisement):
    advertisement_list = [key + ": " + advertisement[key] for key in advertisement.keys()]
    return '\n'.join(advertisement_list)

def construct_message(advertisement, owner, type):
    return """\
Subject: Notification for advertisement {}

Hi,
This message was send because of the following event:
Type: {}
Avertisement: 
{}
Advertisement owner: {}""".format(advertisement["id"], type, advertisement_to_string(advertisement), owner["email"])

def send(user_id: int, advertisement_id: int, owner_id: int, type: str):
    user = httpx.get(USERS_SERVICE_HOST_URL + 'mail/' + str(user_id)).json()
    advertisement = httpx.get(ADVERTISEMENTS_SERVICE_HOST_URL + 'advertisements/' + str(advertisement_id) + '/').json()
    owner = httpx.get(USERS_SERVICE_HOST_URL + 'mail/' + str(owner_id)).json()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, user["email"], construct_message(advertisement, owner, type))

@celery.task(name="send_email")
def send_email(advertisement_id: int, owner_id: int, type: str):
    users = get_users(advertisement_id, owner_id)
    for user in users:
        send(user, advertisement_id, owner_id, type)
    return True
