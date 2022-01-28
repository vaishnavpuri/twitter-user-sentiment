import os
import tweepy as tp
import time
from datetime import datetime
from dotenv import load_dotenv

#constants
PATH = os.path.expanduser('~')+ '/'
env_file = '.env'
today = datetime.today().strftime('%Y-%m-%d')

#read env file
def env_read(env_path):
    if not load_dotenv(env_path):
        return print('env file not found')
    return print('env loaded')

env_read(os.getcwd()+ '/' + env_file)

#connec to twitter
def connect_twitter(api_key, secret_key, access_token, secret_access_token):
    auth = tp.OAuthHandler(
        consumer_key= api_key,
        consumer_secret=secret_key
    )
    auth.set_access_token(
        key = access_token,
        secret = secret_access_token
    )
    api = tp.API(auth)

    try:
        api.verify_credentials()
        print("Connection to Twitter established")
    except:
        print("Failed to connect")
    return api

api = connect_twitter( 
    api_key= os.getenv("API_KEY"),
    secret_key = os.getenv("API_SECRET"),
    access_token = os.getenv("ACCESS_TOKEN"),
    secret_access_token = os.getenv("TOKEN_SECRET")
)