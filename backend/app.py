from flask import Flask, request
from run_model import predict_review_scores

app = Flask(__name__)

@app.route("/score", methods=['POST'])
def score():
    data = request.get_json()
    review = data.get('review', '')

    print(f'get review: {review}')

    # Use the predict_review_scores function to get the score
    scores = predict_review_scores([review])

    return {"score": scores[0]}
