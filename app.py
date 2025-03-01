import os
import glob
import platform
import ctypes
import logging
from flask import Flask, request, jsonify
import numpy as np
from altrustworthyai.glassbox import ExplainableBoostingClassifier
from data_loader import load_and_preprocess_data

# Configure logging for verbose output
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# --- Dynamic Library Lookup Patch ---
def load_libebm():
    """
    Dynamically locate the shared library required for high-performance boosting computations.
    This library underpins the model’s ability to generate transparent predictions and fairness metrics,
    which are essential for AI risk assessment.
    """
    override = os.environ.get("LIBEBM_PATH")
    if override:
        logger.info(f"Using LIBEBM_PATH override: {override}")
        if os.path.exists(override):
            return override
        else:
            raise RuntimeError(f"LIBEBM_PATH is set to {override}, but that file does not exist.")
    project_root = os.path.abspath(os.path.dirname(__file__))
    base_dir = os.path.join(project_root, "altrustworthyai", "shared", "libebm")
    logger.info(f"Looking for libebm files in {base_dir}")
    system = platform.system()
    machine = platform.machine()
    logger.info(f"Detected system: {system}, architecture: {machine}")
    if system == "Darwin" and machine == "arm64":
        pattern = os.path.join(base_dir, "libebm_mac_arm*.dylib")
    elif system == "Darwin":
        pattern = os.path.join(base_dir, "libebm_mac*.dylib")
    elif system == "Linux":
        pattern = os.path.join(base_dir, "libebm_linux*.so")
    elif system == "Windows":
        pattern = os.path.join(base_dir, "libebm_windows*.dll")
    else:
        raise RuntimeError("Unsupported system")
    matches = glob.glob(pattern)
    if not matches:
        raise RuntimeError(f"Could not find a libebm library matching pattern: {pattern}")
    chosen_lib = matches[0]
    logger.info(f"Selected libebm library: {chosen_lib}")
    return chosen_lib

from altrustworthyai.utils._native import Native
Native._get_ebm_lib_path = staticmethod(lambda debug=True: load_libebm())
# --- End Dynamic Patch ---

# Load the shared library
try:
    if "libebm" not in os.environ.get("LOADED_LIBS", ""):
        libebm_path = Native._get_ebm_lib_path(debug=True)
        ctypes.CDLL(libebm_path)
        logger.info(f"✅ Successfully loaded {os.path.basename(libebm_path)}")
        lib_directory = os.path.dirname(libebm_path)
        os.environ["LD_LIBRARY_PATH"] = lib_directory
        os.environ["DYLD_LIBRARY_PATH"] = lib_directory
        os.environ["LOADED_LIBS"] = "libebm"
except Exception as e:
    logger.error(f"⚠️ Failed to load libebm: {e}")
    raise RuntimeError("Critical error: Could not load libebm.")

# Initialize Flask app and load dataset/model.
# The dataset is preprocessed so that the first 14 columns serve as features and the 15th column ('income') is the binary target.
app = Flask(__name__)
logger.info("🔹 Before creating dataset...")
X_train, X_test, y_train, y_test = load_and_preprocess_data()

# Use a reduced training subset for faster development.
X_train = X_train[:100]
y_train = y_train[:100]

logger.info("🔹 Training model with reduced dataset...")
model = ExplainableBoostingClassifier()
model.fit(X_train, y_train)
logger.info("✅ Model training completed successfully.")

@app.route("/predict", methods=["POST"])
def predict():
    """
    Generate a binary income prediction.
    The model expects a feature vector with 14 elements (all columns except the target 'income').
    If 15 values are received (i.e. the target is inadvertently included), the last value is removed.
    This ensures that predictions are based on the proper input, supporting accurate fairness assessment.
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
    The explanation includes feature names and their importance scores, which are essential for understanding
    how protected attributes (e.g., age, gender, race) impact the income prediction. These metrics are critical
    for AI risk assessment and fairness evaluation.
    """
    explanation = model.explain_global()
    logger.debug("Global explanation generated successfully.")
    logger.info("Fairness Assessment: Inspect protected attributes (e.g., age, race, sex) from explanation scores.")
    return jsonify({"explanation": explanation.data()})

if __name__ == "__main__":
    logger.info("Starting ALTrustworthyAI Adult App on port 5002...")
    app.run(host="0.0.0.0", port=5002)
