from flask import Flask, jsonify
from fetch_data import (firebase_db, currentYear, currentMonth)
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def main():
    data = firebase_db.child(currentYear).child(currentMonth).get()
    data_keys = [tweet.key() for tweet in data.each()]
    data_vals = [tweet.val() for tweet in data.each()]
    data = dict(zip(data_keys, data_vals))
    return jsonify(data), 200
