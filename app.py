import logging
import numpy as np

from flask import Flask, request, jsonify
from interpret.glassbox import ExplainableBoostingClassifier as ALTrustworthyEBM

from data_loader import load_and_preprocess_data

# Configure logging for verbose output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
logger.info("🔹 Before creating dataset...")

# Load & preprocess data
X_train, X_test, y_train, y_test = load_and_preprocess_data()

# Use a reduced training subset for faster development
X_train = X_train[:100]
y_train = y_train[:100]

logger.info("🔹 Training model with reduced dataset...")
model = ALTrustworthyEBM()
model.fit(X_train, y_train)
logger.info("✅ Model training completed successfully.")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Generate a binary income prediction using the EBM model.
    The model expects a feature vector with 14 elements (all columns except the target 'income').
    If 15 values are received (i.e. the target is inadvertently included), the last value is removed.
    """
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
    """
    Retrieve a global explanation of the model.
    The explanation includes feature names and their importance scores, which are crucial
    for understanding how protected attributes (e.g., age, gender, race) impact the prediction.
    """
    explanation = model.explain_global()
    logger.debug("Global explanation generated successfully.")
    logger.info("Fairness Assessment: Inspect protected attributes from explanation scores.")
    return jsonify({"explanation": explanation.data()})

if __name__ == "__main__":
    logger.info("Starting ALTrustworthyAI Adult App on port 5002...")
    app.run(host="0.0.0.0", port=5002)
