import os
os.environ["FORCE_DYNAMIC_LIBEBM"] = "true"

import glob
import platform
import logging
import importlib
import unittest

from altrustworthyai.utils._native import Native

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test_app")

def load_libebm():
    override = os.environ.get("LIBEBM_PATH")
    if override and os.path.exists(override):
        return override
    system = platform.system()
    machine = platform.machine()
    base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "altrustworthyai", "shared", "libebm")
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
    return matches[0]

Native._get_ebm_lib_path = staticmethod(lambda debug=True: load_libebm())

app_module = importlib.import_module("app")
flask_app = app_module.app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = flask_app.test_client()
        self.client.testing = True

    def test_predict_endpoint_14_features(self):
        response = self.client.post("/predict", json={
            "features": [30, "State-gov", 141297, "Bachelors", 13,
                         "Married-civ-spouse", "Prof-specialty", "Husband",
                         "Asian-Pac-Islander", "Male", 0, 0, 40, "India"]
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("prediction", data)
        self.assertEqual(len(data["prediction"]), 1)

    def test_predict_endpoint_15_features(self):
        with self.assertLogs("app", level="WARNING") as log_cm:
            response = self.client.post("/predict", json={
                "features": [30, "State-gov", 141297, "Bachelors", 13,
                             "Married-civ-spouse", "Prof-specialty", "Husband",
                             "Asian-Pac-Islander", "Male", 0, 0, 40, "India", ">50K"]
            })
            self.assertEqual(response.status_code, 200)
            self.assertTrue(any("Received 15 features" in m for m in log_cm.output))

    def test_explain_endpoint(self):
        response = self.client.get("/explain")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("explanation", data)
        self.assertIn("names", data["explanation"])
        self.assertIn("scores", data["explanation"])

    def test_compare_endpoint(self):
        response = self.client.get("/compare")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("comparison", data)
        self.assertIn("EBM_mean_accuracy", data["comparison"])
        self.assertIn("Baseline_LogisticRegression_mean_accuracy", data["comparison"])
        self.assertIsInstance(data["comparison"]["EBM_cv_scores"], list)

if __name__ == "__main__":
    unittest.main()
