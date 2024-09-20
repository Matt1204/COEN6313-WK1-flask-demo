from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/")
def read_root():
    return {"Hello": "World"}

@app.route("/predict_img_url", methods=["POST"])
def predict_img_url():
    url = request.args.get('url', None) # getting query params

    if not url:
        return jsonify({"error": "URL is required"}), 400

    req_url = os.getenv("REQ_URL")
    req_url += 'url'
    prediction_key = os.getenv("PREDICTION_KEY")

    # req_url = "https://coen6313-instance-0919.cognitiveservices.azure.com/customvision/v3.0/Prediction/d7d96e92-0d0d-4024-9803-bc5d74e1d7e8/classify/iterations/proj1-iteration1/url"
    headers = {
        'Content-Type': 'application/json',
        'Prediction-Key': prediction_key
    }
    payload = {"Url": url}

    try:
        response = requests.post(req_url, headers=headers, json=payload)
        if response.status_code == 200:
            return jsonify(response.json()), 200 # convert data to JSON
        else:
            return jsonify({"error": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict_img_file", methods=["POST"])
def predict_img_file():
    if 'file' not in request.files:
        return jsonify({"error": "File is required"}), 400
    file = request.files['file']

    # req_url = "https://coen6313-instance-0919.cognitiveservices.azure.com/customvision/v3.0/Prediction/d7d96e92-0d0d-4024-9803-bc5d74e1d7e8/classify/iterations/proj1-iteration1/image"
    req_url = os.getenv("REQ_URL")
    req_url += 'image'
    prediction_key = os.getenv("PREDICTION_KEY")
    headers = {
        # 'Content-Type': 'application/octet-stream',
        'Prediction-Key': prediction_key
    }
    payload = file.read()

    try:
        response = requests.post(req_url, headers=headers, data=payload)
        if response.status_code == 200:
            return jsonify(response.json()), 200
        else:
            return jsonify({"error": response.text}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
