from flask import Flask, render_template
from fetch_data import (firebase_db, firebase_user, currentYear)

app = Flask(__name__)


@app.route('/')
def main():
    # data = firebase_db.child(currentYear).get(firebase_user['idToken'])
    data = firebase_db.get(firebase_user['idToken'])
    data = [tweet.val() for tweet in data.each()]
    print(data)
    return render_template('base.html', all_tweets=data)
