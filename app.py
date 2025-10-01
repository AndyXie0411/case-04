from datetime import datetime, timezone
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# Ensure data folder exists
DATA_FILE = "data/survey.ndjson"
os.makedirs("data", exist_ok=True)

# --- Existing routes ---
@app.get("/time")
def get_time():
    now_utc = datetime.now(timezone.utc)
    now_local = datetime.now()
    payload = {
        "utc_iso": now_utc.isoformat(),
        "local_iso": now_local.isoformat(),
        "server": "flask-warmup"
    }
    return jsonify(payload), 200

@app.get("/ping")
def ping():
    return jsonify({"message": "API is alive"}), 200

# --- New route required by autograder ---
@app.route("/v1/survey", methods=["POST"])
def submit_survey():
    if not request.is_json:
        return jsonify({"error": "invalid_json"}), 400
    
    data = request.get_json()

    # Append submission to NDJSON file
    with open(DATA_FILE, "a") as f:
        json.dump(data, f)
        f.write("\n")

    return jsonify({"status": "created"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
