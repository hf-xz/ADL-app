from flask import Flask, request
from random import random

app = Flask(__name__)

@app.route("/score", methods=['POST'])
def score():
    data = request.get_json()
    review = data.get('review', '')

    print(f'get review: {review}')

    return {'score': random() * 9 + 1}
