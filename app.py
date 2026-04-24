"""
Iron Ore Quality Predictor — Web App
=====================================
Simple Flask app for predicting % Silica Concentrate.

Usage:
    pip install flask joblib scikit-learn xgboost
    python webapp/app.py
"""

from flask import Flask, request, jsonify, render_template_string
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load models
MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'models')

rf_model      = joblib.load(f"{MODEL_DIR}/random_forest_model.pkl")
xgb_model     = joblib.load(f"{MODEL_DIR}/xgboost_model.pkl")
scaler        = joblib.load(f"{MODEL_DIR}/scaler.pkl")
feature_names = joblib.load(f"{MODEL_DIR}/feature_names.pkl")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Iron Ore Quality Predictor</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; background: #f5f5f5; }
        h1 { color: #2c3e50; border-bottom: 3px solid #e74c3c; padding-bottom: 10px; }
        .form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
        label { font-size: 13px; color: #555; }
        input { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #e74c3c; color: white; padding: 12px 30px; border: none;
                 border-radius: 5px; cursor: pointer; font-size: 16px; margin-top: 20px; }
        button:hover { background: #c0392b; }
        .result { background: white; padding: 20px; border-radius: 8px; margin-top: 20px;
                  border-left: 5px solid #27ae60; }
        .result h2 { color: #27ae60; margin-top: 0; }
        .badge { display: inline-block; background: #2ecc71; color: white;
                 padding: 5px 12px; border-radius: 20px; font-size: 20px; font-weight: bold; }
        .warning { border-left-color: #e67e22; }
        .warning h2 { color: #e67e22; }
        .warning .badge { background: #e67e22; }
    </style>
</head>
<body>
    <h1>🏭 Iron Ore Quality Predictor</h1>
    <p>Enter flotation plant process parameters to predict <strong>% Silica Concentrate</strong></p>

    <form method="POST" action="/predict">
        <div class="form-grid">
            {% for feature in features %}
            <div>
                <label>{{ feature }}</label>
                <input type="number" step="any" name="{{ feature }}" placeholder="e.g. {{ defaults[loop.index0]|round(2) }}" required>
            </div>
            {% endfor %}
        </div>
        <button type="submit">🔍 Predict Silica %</button>
    </form>

    {% if prediction is not none %}
    <div class="result {% if prediction > 2.5 %}warning{% endif %}">
        <h2>Prediction Result</h2>
        <p>Predicted % Silica Concentrate:</p>
        <div class="badge">{{ prediction }}%</div>
        <p style="margin-top:15px; color:#666;">
            {% if prediction < 1.5 %}
            ✅ <strong>Excellent</strong> — Very low silica, high iron purity
            {% elif prediction < 2.5 %}
            ⚠️ <strong>Acceptable</strong> — Monitor and optimize process
            {% else %}
            🔴 <strong>High Silica</strong> — Adjust process parameters
            {% endif %}
        </p>
    </div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    defaults = [55.2, 16.9, 3082, 557, 395, 10.1, 1.79,
                250, 252, 253, 254, 255, 256, 257,
                450, 451, 452, 453, 454, 455, 456,
                64.5]
    return render_template_string(HTML_TEMPLATE, features=feature_names, defaults=defaults, prediction=None)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        values = [float(request.form[f]) for f in feature_names]
        X = np.array(values).reshape(1, -1)
        X_scaled = scaler.transform(X)
        prediction = round(float(xgb_model.predict(X_scaled)[0]), 4)
        defaults = values
        return render_template_string(HTML_TEMPLATE,
                                      features=feature_names,
                                      defaults=defaults,
                                      prediction=prediction)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """JSON API endpoint"""
    data = request.json
    values = [float(data[f]) for f in feature_names]
    X = np.array(values).reshape(1, -1)
    X_scaled = scaler.transform(X)
    rf_pred  = float(rf_model.predict(X)[0])
    xgb_pred = float(xgb_model.predict(X_scaled)[0])
    return jsonify({
        "random_forest_prediction": round(rf_pred, 4),
        "xgboost_prediction": round(xgb_pred, 4),
        "unit": "% Silica Concentrate"
    })

if __name__ == '__main__':
    print("🚀 Starting Iron Ore Quality Predictor Web App...")
    print("   Open: http://localhost:5000")
    app.run(debug=True, port=5000)
