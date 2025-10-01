from datetime import datetime, timezone
from flask import Flask, request, jsonify

app = Flask(__name__)

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

# --- Add this POST route for the survey ---
@app.route("/v1/survey", methods=["POST"])
def submit_survey():
    if not request.is_json:
        return jsonify({"error": "invalid_json"}), 400
    data = request.get_json()
    # TODO: store the data somewhere (e.g., a list or database)
    return jsonify({"status": "created"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

