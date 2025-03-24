import os
# Enable dynamic library lookup for tests.
os.environ["FORCE_DYNAMIC_LIBEBM"] = "true"

import glob
import platform
import logging
import importlib
import unittest
import json

from altrustworthyai.utils._native import Native

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_libebm():
    """
    Locate the shared library using the project structure.
    Ensures that the same native library is used in both testing and production,
    which is crucial for consistency in AI risk assessment outputs.
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

# Inject our custom library loader
Native._get_ebm_lib_path = staticmethod(lambda debug=True: load_libebm())

# Import the Flask application now that EBM path is set
app_module = importlib.import_module("app")
flask_app = app_module.app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = flask_app.test_client()
        self.client.testing = True

    def test_predict_endpoint_14_features(self):
        """
        Test Case: Submitting exactly 14 features should return a single prediction item.
        Prerequisites:
        - The app is running with a loaded EBM model.
        Inputs:
        - A JSON payload containing 14 features (no target).
        Expected Outcome:
        - Status code 200, JSON with key 'prediction' containing exactly one element.
        """
        payload = {
            "features": [
                30, "State-gov", 141297, "Bachelors", 13,
                "Married-civ-spouse", "Prof-specialty", "Husband",
                "Asian-Pac-Islander", "Male", 0, 0, 40, "India"
            ]
        }
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("prediction", data)
        self.assertIsInstance(data["prediction"], list)
        self.assertEqual(len(data["prediction"]), 1)

    def test_predict_endpoint_15_features(self):
        """
        Test Case: Submitting 15 features (including target) should discard the 15th and log a warning.
        """
        payload = {
            "features": [
                30, "State-gov", 141297, "Bachelors", 13,
                "Married-civ-spouse", "Prof-specialty", "Husband",
                "Asian-Pac-Islander", "Male", 0, 0, 40, "India", ">50K"
            ]
        }

        # Listen to the logger in app.py (assumed to be named "app")
        with self.assertLogs("app", level="WARNING") as log_cm:
            response = self.client.post("/predict", json=payload)
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn("prediction", data)
            self.assertIsInstance(data["prediction"], list)
            self.assertEqual(len(data["prediction"]), 1)

        # Confirm the warning is in the logs
        found_warning = any("Received 15 features; assuming last value is the target" in message
                            for message in log_cm.output)
        self.assertTrue(found_warning, "Expected warning log message not found.")

    def test_explain_endpoint(self):
        """
        Test Case: /explain endpoint should return a global explanation
        with keys 'names' and 'scores'.
        Prerequisites:
        - The app is running with a loaded EBM model.
        Inputs:
        - No JSON payload (GET request).
        Expected Outcome:
        - Status code 200, JSON 'explanation' object containing lists 'names' and 'scores'.
        """
        response = self.client.get("/explain")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("explanation", data)
        explanation = data["explanation"]
        self.assertIn("names", explanation)
        self.assertIn("scores", explanation)
        self.assertIsInstance(explanation["names"], list)
        self.assertIsInstance(explanation["scores"], list)

if __name__ == '__main__':
    unittest.main()
