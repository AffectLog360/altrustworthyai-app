import logging
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify
from interpret.glassbox import ExplainableBoostingClassifier as ALTrustworthyEBM
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from data_loader import load_and_preprocess_data

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("app")

# Initialize Flask app
app = Flask(__name__)
logger.info("🔹 Before creating dataset...")

# Load dataset
X_train, X_test, y_train, y_test = load_and_preprocess_data()

# Subsample for development
X_train_small = X_train[:100]
y_train_small = y_train[:100]

# Train EBM model
logger.info("🔹 Training ExplainableBoostingClassifier...")
model = ALTrustworthyEBM()
model.fit(X_train_small, y_train_small)
logger.info("✅ EBM training done.")

# Encode features for baseline model
X_train_encoded = pd.get_dummies(X_train_small)
X_test_encoded = pd.get_dummies(X_test)
X_test_encoded = X_test_encoded.reindex(columns=X_train_encoded.columns, fill_value=0)

# Train baseline model
logger.info("🔹 Training baseline LogisticRegression for /compare...")
baseline_model = LogisticRegression(max_iter=500)
baseline_model.fit(X_train_encoded, y_train_small)
logger.info("✅ Baseline model trained.")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = np.array(data["features"]).reshape(1, -1)
    if features.shape[1] == 15:
        logger.warning("Received 15 features; assuming last value is the target and removing it.")
        features = features[:, :-1]
    prediction = model.predict(features).tolist()
    logger.debug(f"Prediction result: {prediction}")
    return jsonify({"prediction": prediction})

@app.route("/explain", methods=["GET"])
def explain():
    explanation = model.explain_global()
    logger.debug("Global explanation generated successfully.")
    logger.info("Fairness Assessment: Inspect protected attributes from explanation scores.")
    return jsonify({"explanation": explanation.data()})

@app.route("/compare", methods=["GET"])
def compare_models():
    logger.info("🔎 Running model comparison with 5-fold cross-validation...")
    ebm_scores = cross_val_score(model, X_train_small, y_train_small, cv=5, scoring="accuracy")
    baseline_scores = cross_val_score(baseline_model, X_train_encoded, y_train_small, cv=5, scoring="accuracy")

    ebm_mean = float(np.mean(ebm_scores))
    baseline_mean = float(np.mean(baseline_scores))
    logger.info(f"✅ Model comparison complete. EBM accuracy: {ebm_mean:.4f}, LogisticRegression accuracy: {baseline_mean:.4f}")

    return jsonify({
        "comparison": {
            "EBM_mean_accuracy": ebm_mean,
            "Baseline_LogisticRegression_mean_accuracy": baseline_mean,
            "EBM_cv_scores": ebm_scores.tolist(),
            "Baseline_LogisticRegression_cv_scores": baseline_scores.tolist()
        }
    })

if __name__ == "__main__":
    logger.info("Starting ALTrustworthyAI App on port 5002...")
    app.run(host="0.0.0.0", port=5002)
