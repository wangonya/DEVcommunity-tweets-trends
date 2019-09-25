import os
import threading
import schedule
import time
import pyrebase

import tweepy as tw

from datetime import datetime

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

twitter_auth = tw.OAuthHandler(consumer_key, consumer_secret)
twitter_auth.set_access_token(access_token, access_token_secret)
api = tw.API(twitter_auth, wait_on_rate_limit=True)

search_words = '#DEVcommunity'
date_since = datetime.now().strftime('%Y-%m-%d')

firebase_config = {
  'apiKey': os.getenv('FIREBASE_API_KEY'),
  'authDomain': os.getenv('FIREBASE_AUTH_DOMAIN'),
  'databaseURL': os.getenv('FIREBASE_DB_URL'),
  'storageBucket': ''
}

firebase = pyrebase.initialize_app(firebase_config)
firebase_auth = firebase.auth()
firebase_user = firebase_auth.sign_in_with_email_and_password(
        os.getenv('FIREBASE_USER_EMAIL'), os.getenv('FIREBASE_USER_PASSWORD'))
firebase_user_token = firebase_user['idToken']
firebase_db = firebase.database()

currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year


def fetch_data():
    print('fetching data...')
    data = tw.Cursor(api.search, q=search_words, since=date_since).items()
    return data


def run_threaded(job):
    job_thread = threading.Thread(target=job)
    job_thread.start()


def update_data():
    data = {'all_tweets': sum(1 for _ in fetch_data())}
    firebase_db.child(currentYear).child(currentMonth).child(currentDay).set(
        data, firebase_user_token)
    print('data updated')


if __name__ == '__main__':
    # schedule.every(1).hour.do(run_threaded, update_data)
    schedule.every(1).minutes.do(run_threaded, update_data)

    while True:
        schedule.run_pending()
        time.sleep(1)
