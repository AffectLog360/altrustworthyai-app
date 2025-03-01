import os
# Enable dynamic library lookup for tests.
os.environ["FORCE_DYNAMIC_LIBEBM"] = "true"

import glob
import platform
import logging
import importlib

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from altrustworthyai.utils._native import Native

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

Native._get_ebm_lib_path = staticmethod(lambda debug=True: load_libebm())

# Safely import the Flask application module.
app_module = importlib.import_module("app")
flask_app = app_module.app

import unittest
import json

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = flask_app.test_client()
        self.client.testing = True

    def test_predict_endpoint(self):
        """
        Tests the /predict endpoint.
        This endpoint should return a valid binary income prediction after automatically
        adjusting the input (if the complete row including the target is provided).
        This test verifies that the prediction process supports fairness assessment by ensuring
        that the model operates on the expected feature set.
        """
        # Provide 14 features (target is not included).
        payload = {"features": [30, "State-gov", 141297, "Bachelors", 13, "Married-civ-spouse",
                                 "Prof-specialty", "Husband", "Asian-Pac-Islander", "Male", 0, 0, 40, "India"]}
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("prediction", data)
        self.assertIsInstance(data["prediction"], list)
        self.assertEqual(len(data["prediction"]), 1)

    def test_explain_endpoint(self):
        """
        Tests the /explain endpoint.
        This endpoint should return a global explanation that includes feature names and importance scores.
        The explanation output is used to evaluate the influence of protected attributes (e.g., age, race, sex)
        on the model’s decisions, which is critical for assessing fairness.
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
