import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

try:
    from . import util
except ImportError:
    import util

BASE_DIR = Path(__file__).resolve().parent
CLIENT_DIR = BASE_DIR.parent / "client"

app = Flask(__name__, static_folder=str(CLIENT_DIR), static_url_path="")
util.load_saved_artifacts()


@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response


@app.route("/", methods=["GET"])
def index():
    return send_from_directory(CLIENT_DIR, "app.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    return jsonify({
        'locations': util.get_location_names()
    })


@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    payload = request.get_json(silent=True) or request.form

    try:
        total_sqft = float(payload.get("total_sqft", ""))
        location = str(payload.get("location", "")).strip()
        bhk = int(payload.get("bhk", ""))
        bath = int(payload.get("bath", ""))
    except (TypeError, ValueError):
        return jsonify({"error": "total_sqft, bhk, bath, and location are required"}), 400

    if total_sqft <= 0 or bhk <= 0 or bath <= 0:
        return jsonify({"error": "total_sqft, bhk, and bath must be positive values"}), 400

    if not location:
        return jsonify({"error": "location is required"}), 400

    return jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=port, debug=debug)
