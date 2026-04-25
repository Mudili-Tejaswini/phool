"""
Phool Intelligence — Flask Web Application
Serves the price intelligence dashboard and prediction API.
"""

import os
from flask import Flask, render_template, request, jsonify
from src.predictor import PricePredictor

app = Flask(__name__, static_folder="assets", template_folder=".")

# Load model once at startup
predictor = PricePredictor(model_path="models/random_forest.pkl")


@app.route("/")
def index():
    """Serve the main dashboard."""
    return app.send_static_file("../phool-intelligence.html")


@app.route("/api/predict", methods=["POST"])
def predict():
    """
    POST /api/predict
    Body (JSON):
      {
        "shape":  "Anarkali",
        "sleeve": "Long Sleeves",
        "hem":    "Curved",
        "neck":   "Round Neck",
        "length": "Ankle Length",
        "fabric": "Georgette",
        "slit":   "Side Slits",
        "sizes":  6
      }
    Returns:
      { "price": 880, "low": 792, "high": 968, "std": 1012, "premium": 1144 }
    """
    data = request.get_json(force=True)

    required = ["shape", "sleeve", "hem", "neck", "length", "fabric", "slit", "sizes"]
    missing = [k for k in required if k not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        result = predictor.predict(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health")
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "model": predictor.model_name})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
